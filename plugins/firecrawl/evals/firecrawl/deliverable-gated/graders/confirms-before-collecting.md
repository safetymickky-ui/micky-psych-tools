---
# Today's Path C step 1: confirm the workflow and the final artifact with the user first.
type: regex
target: last_message
pattern: '(?:confirm|which|what|how many|should I|do you want|would you like)[^\n?]{0,200}\?'
flags: i
weight: 2
---
