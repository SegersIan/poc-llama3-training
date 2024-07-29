---
title: Debugging "Terminating" kubernetes namespaces
summary: A debug journey about kubernetes namespaces what are stuck in the "terminating" state.
date: 2021-11-25
tags: 
  - Kubernetes
  - Azure
  - AKS
  - Neptune
---

I liked to keep notes while I debug any issues, sometimes they can turn into a blog post. This is one of such notes while I was debugging why a certain Kubernetes (k8s) namespace was stuck terminating. I knew the "quick fix" how to resolve it (removing the finalizers of the `namespace`), but I like to get to the root of an issue. 

**Background Info:** We have REST APIs that allow to us to provision our workloads on top of AKS and other Azure services. Every 12h we run end2end tests that test these REST APIs. When the e2e test completes, we deleted the provisioned workload (using also our own REST API). If the test fails, we also schedule a deletion for that provisioned workload. Sometimes these tests fail and raise our attention.

**Note:** _When I share YAML dumps, I redact verbose information to maintain focus._

## TL;DR;

I follow the leads of finalizers and `status.conditions` via the `namespace` > `pvc` > `pv` > `pod`. Found an orphan `pod` where the owning `statefulset` was not existing anymore. We don't find the cause how the `statefulset` could've been deleted without also deleting the `pod`s related to it. We also discover that there was a `node` provisioned by the autoscaler, but this `node` failed to schedule any `k8s` workloads, no cause found for that either. However, the autoscaller does remove automically fauly `node`s because no workloads are scheduled on it.

## The Problem

After a failing e2e test, it came to my attention that I had a `namespace` in the terminating phase for 4 days straight. This is not the first time happening, the first few times I fixed this issue by removing the `metadata.finalizers` of the terminating `namespace`. 

However, it was time to dig deeper, because I had no idea what these "finalizers" were, how do they work, because, how safe is this fix even? 

```sh
kubectl get ns
NAME                              STATUS        AGE
ns-e2e-1637457951133-scenario-1   Terminating   4d13h
```

Follow me on my investigative journey!

## The Investigation

### The Namespace

First things first, let's have a look at the details of our `namespace`.

```sh
kubectl get ns ns-e2e-1637457951133-scenario-1 -o yaml
```

Let me highlight all the interesting points:

* Namespace was deleted ~30min after creation at `2021-11-21T01:55:16Z`
  ```yaml
  metadata:
    creationTimestamp: "2021-11-21T01:27:08Z"
    deletionTimestamp: "2021-11-21T01:55:16Z"
  ```
* There is a `kuberentes` [finalizer](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/) listed which keeps it from being deleted.
  ```yaml
  spec:
    finalizers:
    - kubernetes
  ```
* Why is this finalizer not removed yet ? Well, our `status.conditions` array sure can help us with that. Let's take in account that at `2021-11-21T01:55:16Z` we tried to delete our namespace.
  ```yaml
    - lastTransitionTime: "2021-11-21T01:55:23Z"
      message: All resources successfully discovered
      reason: ResourcesDiscovered
      status: "False"
      type: NamespaceDeletionDiscoveryFailure
    - lastTransitionTime: "2021-11-21T01:55:23Z"
      message: All legacy kube types successfully parsed
      reason: ParsedGroupVersions
      status: "False"
      type: NamespaceDeletionGroupVersionParsingFailure
    - lastTransitionTime: "2021-11-21T01:55:53Z"
      message: 'Failed to delete all resource types, 1 remaining: unexpected items still
        remain in namespace: ns-e2e-1637457951133-scenario-1 for gvr: /v1, Resource=pods'
      reason: ContentDeletionFailed
      status: "True"
      type: NamespaceDeletionContentFailure
    - lastTransitionTime: "2021-11-21T01:55:23Z"
      message: 'Some resources are remaining: persistentvolumeclaims. has 1 resource
        instances, pods. has 1 resource instances'
      reason: SomeResourcesRemain
      status: "True"
      type: NamespaceContentRemaining
    - lastTransitionTime: "2021-11-21T01:55:23Z"
      message: 'Some content in the namespace has finalizers remaining: kubernetes.io/pvc-protection
        in 1 resource instances'
      reason: SomeFinalizersRemain
      status: "True"
      type: NamespaceFinalizersRemaining
  ```

Those **3 last** conditions give us some hints.

```yaml
  - lastTransitionTime: "2021-11-21T01:55:53Z"
    message: 'Failed to delete all resource types, 1 remaining: unexpected items still
      remain in namespace: ns-e2e-1637457951133-scenario-1 for gvr: /v1, Resource=pods'
  - lastTransitionTime: "2021-11-21T01:55:23Z"
    message: 'Some resources are remaining: persistentvolumeclaims. has 1 resource
      instances, pods. has 1 resource instances'
  - lastTransitionTime: "2021-11-21T01:55:23Z"
    message: 'Some content in the namespace has finalizers remaining: kubernetes.io/pvc-protection
      in 1 resource instances'
```

My attention first is drawn to `finalizers remaining: kubernetes.io/pvc-protection`. So let's investigate those.

### The PVC

List the `pvc`'s within our `namespace`.

```sh
kubectl get pvc -n ns-e2e-1637457951133-scenario-1                                                                                                                                                      
NAME                               STATUS        VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS               AGE
pvc-e2e-1637457951133-scenario-1   Terminating   pvc-faafd179-7122-420a-aaa0-9ddea3598e0d   101Gi      RWX            azurefile-premium-custom   4d14h

...lets get the details...
k get pvc -n ns-e2e-1637457951133-scenario-1 pvc-e2e-1637457951133-scenario-1 -o yaml
```
```yaml
metadata:
  creationTimestamp: "2021-11-21T01:27:08Z"
  deletionGracePeriodSeconds: 0
  deletionTimestamp: "2021-11-21T01:55:16Z"
  finalizers:
  - kubernetes.io/pvc-protection
```

We have the `kuberbetes.io/pvc-protection` finalizer present. Exactly like one of the `status.conditions` entries specified. Let's also inspect the related `pv` then.

### The PV

```sh
kubectl get pv pvc-faafd179-7122-420a-aaa0-9ddea3598e0d -o yaml
```
```yaml
metadata:
  creationTimestamp: "2021-11-21T01:27:09Z"
  deletionGracePeriodSeconds: 0
  deletionTimestamp: "2021-11-21T01:55:16Z"
  finalizers:
  - kubernetes.io/pv-protection
spec:
status:
  phase: Bound
```

Both our `pvc` and `pv` have finalizers which keeps them from being deleted. The `finalizers` [documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/#how-finalizers-work) states:

> When a PersistentVolume object is in use by a Pod, Kubernetes adds the pv-protection finalizer. If you try to delete the PersistentVolume, it enters a Terminating status, but the controller can't delete it because the finalizer exists. When the Pod stops using the PersistentVolume, Kubernetes clears the pv-protection finalizer, and the controller deletes the volume.

Oh, do we have still a `pod` running? Well, if we look again at our `namespace.status.conditions` there was actually entries that mentioned something about a `pod`:

```yaml
  - lastTransitionTime: "2021-11-21T01:55:53Z"
    message: 'Failed to delete all resource types, 1 remaining: unexpected items still
      remain in namespace: ns-e2e-1637457951133-scenario-1 for gvr: /v1, Resource=pods'
  - lastTransitionTime: "2021-11-21T01:55:23Z"
    message: 'Some resources are remaining: persistentvolumeclaims. has 1 resource
      instances, pods. has 1 resource instances'
```

I must say, that I totally overread the `pod` related messages. Either way, we got a lead, let's inspect our `pod`s.

### The Pod

Looking for any pods in our `namespace`:

```sh
kubectl get pods -n ns-e2e-1637457951133-scenario-1
NAME                                     READY   STATUS        RESTARTS   AGE
pod/sts-e2e-1637457951133-scenario-1-0   0/1     Terminating   0          4d13h
```

Gotcha! Let's see why our pod is not terminating.

```sh
kubectl get pod -n ns-e2e-1637457951133-scenario-1 sts-e2e-1637457951133-scenario-1-0 -o yaml
```
```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2021-11-21T01:55:14Z"
  deletionGracePeriodSeconds: 30
  deletionTimestamp: "2021-11-21T01:55:47Z"
  ownerReferences:
  - apiVersion: apps/v1
    blockOwnerDeletion: true
    controller: true
    kind: StatefulSet
    name: sts-e2e-1637457951133-scenario-1
    uid: 1f9b6f3b-6d62-48a7-bae6-d6e461c769a9
status:
  conditions:
  - lastProbeTime: null
    lastTransitionTime: "2021-11-21T01:55:15Z"
    status: "True"
    type: Initialized
  - lastProbeTime: null
    lastTransitionTime: "2021-11-21T01:56:24Z"
    message: 'containers with unready status: [planet9]'
    reason: ContainersNotReady
    status: "False"
    type: Ready
  - lastProbeTime: null
    lastTransitionTime: "2021-11-21T01:56:24Z"
    message: 'containers with unready status: [planet9]'
    reason: ContainersNotReady
    status: "False"
    type: ContainersReady
  - lastProbeTime: null
    lastTransitionTime: "2021-11-21T01:55:15Z"
    status: "True"
    type: PodScheduled
  containerStatuses:
  - image: neptunesoftware/planet9:v21.6.0
    imageID: ""
    lastState: {}
    name: planet9
    ready: false
    restartCount: 0
    started: false
    state:
      waiting:
        reason: ContainerCreating
  phase: Pending
```

Here we see no finalizers, this might be the main object that blocks things from deleting!
If we look closer to the `pod.status.conditions` entries:

```yaml
  - lastProbeTime: null
    lastTransitionTime: "2021-11-21T01:55:15Z"
    status: "True"
    type: Initialized
  - lastProbeTime: null
    lastTransitionTime: "2021-11-21T01:56:24Z"
    message: 'containers with unready status: [planet9]'
    reason: ContainersNotReady
    status: "False"
    type: Ready
  - lastProbeTime: null
    lastTransitionTime: "2021-11-21T01:56:24Z"
    message: 'containers with unready status: [planet9]'
    reason: ContainersNotReady
    status: "False"
    type: ContainersReady
  - lastProbeTime: null
    lastTransitionTime: "2021-11-21T01:55:15Z"
    status: "True"
    type: PodScheduled
```

* We went from `Initialized` > `Ready` > `ContainersReady` > `PodScheduled` for `status.conditions`. For `pod.status.containerStatuses` we can see that we never passed `ContainerCreating`. Why ? Did the node pool fail to schedule this fella? It's time to inspect the `kube events`. 
* There is an `ownerReferences` in our `pod` to our `statefulset` which does not exist anymore (I verified this). This means that, when the `statefulset` is deleted, the `pod`s should be deleted along with it.
  ```yaml
    ownerReferences:
    - apiVersion: apps/v1
      blockOwnerDeletion: true
      controller: true
      kind: StatefulSet
      name: sts-e2e-1637457951133-scenario-1
      uid: 1f9b6f3b-6d62-48a7-bae6-d6e461c769a9
  ```

### Inspecting KubeEvents

We are using AKS (Azure Kubernetes Service), so I can query `KubeEvents` and such from the `Log Analytics Workspace` service of Azure.

Let's have a look at our `KubeEvents` table, looking for all entries in our target `namespace`.
```
KubeEvents
| where not(isempty(Namespace))
| where Namespace == "ns-e2e-1637457951133-scenario-1"
| project TimeGenerated, Name, Reason, Message
| sort by TimeGenerated asc
```
Returned us the following:
```csv
"TimeGenerated [UTC]",Name,Reason,Message
"21/11/2021, 01:27:42.000","cm-acme-http-solver-6ptbx",FailedToUpdateEndpoint,"Failed to update endpoint ns-e2e-1637457951133-scenario-1/cm-acme-http-solver-6ptbx: Operation cannot be fulfilled on endpoints ""cm-acme-http-solver-6ptbx"": StorageError: invalid object, Code: 4, Key: /registry/services/endpoints/ns-e2e-1637457951133-scenario-1/cm-acme-http-solver-6ptbx, ResourceVersion: 0, AdditionalErrorMsg: Precondition failed: UID in precondition: d699309f-8389-4fb3-bb0e-1c4af4521ca5, UID in object meta: "
"21/11/2021, 01:49:42.000","sts-e2e-1637457951133-scenario-1-1",Unhealthy,"Liveness probe failed: HTTP probe failed with statuscode: 500"
"21/11/2021, 01:49:42.000","sts-e2e-1637457951133-scenario-1-0",Unhealthy,"Liveness probe failed: Get ""http://10.244.19.26:8080/healthz"": context deadline exceeded (Client.Timeout exceeded while awaiting headers)"
"21/11/2021, 01:49:42.000","sts-e2e-1637457951133-scenario-1-0",Unhealthy,"Liveness probe failed: HTTP probe failed with statuscode: 500"
"21/11/2021, 01:53:42.000","sts-e2e-1637457951133-scenario-1-1",FailedScheduling,"0/16 nodes are available: 12 Insufficient cpu, 14 Insufficient memory, 2 node(s) didn't match Pod's node affinity."
"21/11/2021, 01:53:42.000","sts-e2e-1637457951133-scenario-1-1",FailedScheduling,"0/16 nodes are available: 12 Insufficient cpu, 14 Insufficient memory, 2 node(s) didn't match Pod's node affinity."
"21/11/2021, 01:54:42.000","sts-e2e-1637457951133-scenario-1-1",FailedScheduling,"0/17 nodes are available: 1 node(s) had taint {node.kubernetes.io/not-ready: }, that the pod didn't tolerate, 12 Insufficient cpu, 14 Insufficient memory, 2 node(s) didn't match Pod's node affinity."
```

Lot's of text and noise, so what draws my attention here:
* So there were 16 `node`s. I know from my cluster configuration that we can scale to 23 `node`s (2 `node` pools, one max 20, other max 3) and I that know autoscaling is enabled and functioning.
  * _I've investigated that on 21/11/2021, the node pool limitations were no different from today, using git log on my Terraform repo of our aks cluster + checking any previous Terraform Cloud plan executions._
* At some point there were actually 17 `node`s.
  ```
  FailedScheduling,"0/17 nodes are available: 1 node(s) had taint {node.kubernetes.io/not-ready: }, that the pod didn't tolerate, 12 Insufficient cpu, 14 Insufficient memory, 2 node(s) didn't match Pod's node affinity.
  ```
  So he tried to scale up, but then failed ? At some point had 0/17 instead of 0/16 nodes available.

**This raises the following 2 questions**

1. Why did the pod failed to start?
2. Why was the `pod` not deleted while the owning `statefulset` was deleted?

#### Question 1: Why did the pod failed to start?

There was a lack of nodes, that we can conclude of the aforementioned `KubeEvents`:
```csv
"21/11/2021, 01:53:42.000","sts-e2e-1637457951133-scenario-1-1",FailedScheduling,"0/16 nodes are available: 12 Insufficient cpu, 14 Insufficient memory, 2 node(s) didn't match Pod's node affinity."
```

The node pool has an auto scaler, and the node pool was not yet at its max. So we should query all of the `KubeEvents` around that time window, so we're ignoring the `namespace`.

```
KubeEvents
| project TimeGenerated, ObjectKind, Name, Reason, Message
| sort by TimeGenerated asc
```
Returned us the following:
```csv
"TimeGenerated [UTC]",ObjectKind,Name,Reason,Message
"21/11/2021, 01:49:42.000",Pod,"sts-e2e-1637457951133-scenario-1-1",Unhealthy,"Liveness probe failed: HTTP probe failed with statuscode: 500"
"21/11/2021, 01:49:42.000",Pod,"sts-e2e-1637457951133-scenario-1-0",Unhealthy,"Liveness probe failed: Get ""http://10.244.19.26:8080/healthz"": context deadline exceeded (Client.Timeout exceeded while awaiting headers)"
"21/11/2021, 01:49:42.000",Pod,"sts-e2e-1637457951133-scenario-1-0",Unhealthy,"Liveness probe failed: HTTP probe failed with statuscode: 500"
"21/11/2021, 01:53:42.000",Pod,"sts-e2e-1637457951133-scenario-1-1",FailedScheduling,"0/16 nodes are available: 12 Insufficient cpu, 14 Insufficient memory, 2 node(s) didn't match Pod's node affinity."
"21/11/2021, 01:53:42.000",Pod,"sts-e2e-1637457951133-scenario-1-1",FailedScheduling,"0/16 nodes are available: 12 Insufficient cpu, 14 Insufficient memory, 2 node(s) didn't match Pod's node affinity."
"21/11/2021, 01:54:42.000",Pod,"omsagent-zfn9g",FailedMount,"MountVolume.SetUp failed for volume ""omsagent-secret"" : failed to sync secret cache: timed out waiting for the condition"
"21/11/2021, 01:54:42.000",Pod,"omsagent-zfn9g",NetworkNotReady,"network is not ready: runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:Network plugin returns error: cni plugin not initialized"
"21/11/2021, 01:54:42.000",Pod,"omsagent-zfn9g",FailedCreatePodSandBox,"Failed to create pod sandbox: rpc error: code = Unknown desc = failed to setup network for sandbox ""3e906c0a60cdcce40039359ee24175d04eb13fde1077ba17d8152ee685bf195d"": stat /var/lib/calico/nodename: no such file or directory: check that the calico/node container is running and has mounted /var/lib/calico/"
"21/11/2021, 01:54:42.000",Pod,"omsagent-zfn9g",FailedMount,"MountVolume.SetUp failed for volume ""settings-vol-config"" : failed to sync configmap cache: timed out waiting for the condition"
"21/11/2021, 01:54:42.000",Pod,"sts-e2e-1637457951133-scenario-1-1",FailedScheduling,"0/17 nodes are available: 1 node(s) had taint {node.kubernetes.io/not-ready: }, that the pod didn't tolerate, 12 Insufficient cpu, 14 Insufficient memory, 2 node(s) didn't match Pod's node affinity."
"21/11/2021, 01:54:42.000",Node,"aks-azsql02v1tmp-21450618-vmss000005",InvalidDiskCapacity,"invalid capacity 0 on image filesystem"
"21/11/2021, 01:54:42.000",Pod,"omsagent-zfn9g",FailedMount,"MountVolume.SetUp failed for volume ""osm-settings-vol-config"" : failed to sync configmap cache: timed out waiting for the condition"
"21/11/2021, 01:55:42.000",Pod,"calico-node-w899p",Unhealthy,"Liveness probe failed: Get ""http://localhost:9099/liveness"": dial tcp 127.0.0.1:9099: connect: connection refused"
"21/11/2021, 02:10:42.000",Pod,"omsagent-zfn9g",NodeNotReady,"Node is not ready"
"21/11/2021, 02:10:42.000",Pod,"kube-proxy-vpbq2",NodeNotReady,"Node is not ready"
"21/11/2021, 02:10:42.000",Pod,"calico-node-w899p",NodeNotReady,"Node is not ready"
"21/11/2021, 02:10:42.000",Pod,"nmi-gcz9s",NodeNotReady,"Node is not ready"

```

Hmmm nothing much, we can see that there was a `node` `aks-azsql02v1tmp-21450618-vmss000005` that had some error, let's see how long that lived...

```
KubeNodeInventory
| where Computer == "aks-azsql02v1tmp-21450618-vmss000005"
| project TimeGenerated, Status
| sort by TimeGenerated asc
```
```csv
"TimeGenerated [UTC]",Status
"21/11/2021, 01:54:42.000",Ready
"21/11/2021, 01:55:42.000",Ready
"21/11/2021, 01:56:42.000",Ready
"21/11/2021, 01:57:42.000",Ready
"21/11/2021, 01:58:42.000",Ready
"21/11/2021, 01:59:42.000",Ready
"21/11/2021, 02:00:42.000",Ready
"21/11/2021, 02:01:42.000",Ready
"21/11/2021, 02:02:42.000",Ready
"21/11/2021, 02:03:42.000",Ready
"21/11/2021, 02:04:42.000",Ready
"21/11/2021, 02:05:42.000",Ready
"21/11/2021, 02:06:42.000",Ready
"21/11/2021, 02:07:42.000",Ready
"21/11/2021, 02:08:42.000",Ready
"21/11/2021, 02:09:42.000",Ready
```
This leads me to believe that a `node` `aks-azsql02v1tmp-21450618-vmss000005` provisioned between `01:54:42` and `02:09:42.000`. This does seem to be around the time our pod tried to schedule. **So... at some point there was enough resource in the node pool for our `pod` to be allocated.**

Ok, let's look at those other entries from before:
```csv
"21/11/2021, 01:54:42.000",Pod,"omsagent-zfn9g",FailedMount,"MountVolume.SetUp failed for volume ""osm-settings-vol-config"" : failed to sync configmap cache: timed out waiting for the condition"
"21/11/2021, 01:55:42.000",Pod,"calico-node-w899p",Unhealthy,"Liveness probe failed: Get ""http://localhost:9099/liveness"": dial tcp 127.0.0.1:9099: connect: connection refused"
"21/11/2021, 02:10:42.000",Pod,"omsagent-zfn9g",NodeNotReady,"Node is not ready"
"21/11/2021, 02:10:42.000",Pod,"kube-proxy-vpbq2",NodeNotReady,"Node is not ready"
"21/11/2021, 02:10:42.000",Pod,"calico-node-w899p",NodeNotReady,"Node is not ready"
"21/11/2021, 02:10:42.000",Pod,"nmi-gcz9s",NodeNotReady,"Node is not ready"
```
There were some other `pod`s having trouble because of a `node` that was not ready... shall we see on which `node` that was?
```
KubePodInventory 
    | where Name in ("omsagent-zfn9g", "calico-node-w899p", "kube-proxy-vpbq2", "nmi-gcz9s")
    | distinct Computer

...returns...

aks-azsql02v1tmp-21450618-vmss000005
```

Well, well, well... clearly this node `aks-azsql02v1tmp-21450618-vmss000005` failed to provision any pod, even the mandatory daemonset pods for networking and diagnostics.

This would indicated that the nodepool scaled with an extra node `aks-azsql02v1tmp-21450618-vmss000005`, but the node was failing to provision any pods, even when reporting `Ready`.

**Conclusion**: I'm not sure how to investigate this any further. However, working with systems and scale, it's realistic things just fail. That's why it's more important to build a resilient system instead of a perfect system with no errors. For now I'll conclude that a faulty node was provisioned by AKS and was then decomminsioned because no pods were scheduled on it. This is the beauty of the autoscaler, it removes nodes that don't schedule any workloads. The faulty node is at least automatically taken out of rotation, the power of k8s!

#### Question 2: Why was the `pod` not deleted while the owning `statefulset` was deleted?

Let's revise what we saw on the `pod`:
```yaml
  ownerReferences:
  - apiVersion: apps/v1
    blockOwnerDeletion: true
    controller: true
    kind: StatefulSet
    name: sts-e2e-1637457951133-scenario-1
    uid: 1f9b6f3b-6d62-48a7-bae6-d6e461c769a9
```
There is a [ownerReferences](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/) block here, that points to the stateful parent statefulset that doesn't exist anymore.

According to the documentation, the `blockOwnerDeletion: true` indicates:

> Dependent objects also have an ownerReferences.blockOwnerDeletion field that takes a boolean value and controls whether specific dependents can block garbage collection from deleting their owner object. Kubernetes automatically sets this field to true if a controller (for example, the Deployment controller) sets the value of the metadata.ownerReferences field. You can also set the value of the blockOwnerDeletion field manually to control which dependents block garbage collection.

So... nothing new we learn from that. What if... I deleted the ownerReferences on my pod ? I first tried the normal way:
```sh
kubectl delete pod -n ns-e2e-1637457951133-scenario-1 sts-e2e-1637457951133-scenario-1-0
...deletion doesn't complete
```
Aarrrgh, let's force delete then
```sh
kubectl delete pod -n ns-e2e-1637457951133-scenario-1 sts-e2e-1637457951133-scenario-1-0 --grace-period=0 --force
warning: Immediate deletion does not wait for confirmation that the running resource has been terminated. The resource may continue to run on the cluster indefinitely.
pod "sts-e2e-1637457951133-scenario-1-0" force deleted
```

I don't like this message:
> The resource may continue to run on the cluster indefinitely.

However, now de `pod` is deleted, the entire `namespace` with the terminating `pvc` and `pv` were all removed by kubernetes.

**Conclusion:** We know that the `pod` was the culprit that kept the entire `namespace` from properly terminating. However, no real root cause was found why the `pod` was not deleted along with owning `statefulset`. The proper references were there between the `pod` and the `statefulset`. All I can see is that the last state of the `container` in our `pod` was `ContainerCreating`. Not sure how to proceed on this, I'll let this reset for a while now.

## Resources

* [Finalizer Docs](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/)
* [Using Finalizers To Control Deletion](https://kubernetes.io/blog/2021/05/14/using-finalizers-to-control-deletion/)
* [Owners and Dependents](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/)
