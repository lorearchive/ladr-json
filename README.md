# LADR-JSON

The Git LFS for the json files used by LADR.

[![Netlify Status](https://api.netlify.com/api/v1/badges/4f014db9-ee9b-4e78-b5da-afccf5f347cc/deploy-status)](https://app.netlify.com/sites/ladr/deploys)


## File names explained
### Main story
Each episodes inside main stories can be divided up like so: `Episode-sector-id.json`. For example, `Episode2-s1-11025.json`

- Different sectors belong in the same episode, however in the game they are divided by combat. I was originally going to name them **parts**, like Part 1, Part 2, etc. but they conflict with the game structure.
- ids are not really cared by the end users.
