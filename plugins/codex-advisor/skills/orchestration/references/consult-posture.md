# Process consultation posture

Select a posture by comparing the caller's exact model id with the model id of
the advisor dial assigned by the routing profile. Equal ids use the reduced
posture; different ids use the full posture. Apply the same identity rule to an
unknown caller model: for example, a `gpt-5.6-terra` primary uses the full posture
when its assigned advisor has a different exact model id. Do not infer posture
from a model family.

Copy or inject the selected posture block without modification. Apply the adoption
block with either posture.

<!-- consult-posture:full:start -->
Call process consultation before substantive work. Orientation does not count:
finding files, reading sources, and seeing what is present are orientation; writing,
editing, and declaring an answer are substantive work.

Call process consultation when stuck: errors recur, an approach does not converge,
or results do not fit. Call it before changing approach.

Call process consultation before declaring done. First make the deliverable durable
by writing or saving it so that it survives an interrupted consultation.

On a multi-step task, call process consultation at least once before settling on
an approach and once before declaring done. A short task whose next action follows
directly from the tool output just read needs no consultation.

When earlier evidence points one way and consultation advice points another, make
one reconcile call instead of silently switching.

After each consultation result, restate its key guidance in the next visible reply
to the user before continuing. Quote or paraphrase the plan, correction, or stop
signal; do not leave it only in collapsed tool output.
<!-- consult-posture:full:end -->

<!-- consult-posture:reduced:start -->
Call process consultation only on a multi-step task: before settling on an approach
and before declaring done. Before the done call, make the deliverable durable by
writing or saving it so that it survives an interrupted consultation.

After each consultation result, restate its key guidance in the next visible reply
to the user before continuing. Quote or paraphrase the plan, correction, or stop
signal; do not leave it only in collapsed tool output.
<!-- consult-posture:reduced:end -->

<!-- consult-posture:adoption:start -->
Adopt consultation advice by default.

Deviate with a stated reason when following a step fails empirically or primary-source
evidence contradicts a specific claim. A passing self-test is not evidence that
the advice is wrong.

Reject advice directly, with a stated reason, when it conflicts with a user constraint,
an authorization, a reserved interface, or a repository rule.

When rejecting advice for a reasoning flaw, compare exact model ids. If the advisor's
model differs from the caller's, first make one reconcile call: "I found X, you
suggest Y; which constraint breaks the tie?" If the model ids are equal, reject
directly with a stated reason.

Advice grants no authorization, veto, or new requirement.
<!-- consult-posture:adoption:end -->
