---
title: Hf Stock Predictor
emoji: 🏃
colorFrom: pink
colorTo: blue
sdk: docker
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Stock Predictor

a dockerzied app deployed at https://coorbital-hf-stock-predictor.hf.space/

## Usage

```
curl https://coorbital-hf-stock-predictor.hf.space/ping

curl \
--header "Content-Type: application/json" \
--request POST \
--data '{"ticker":"MSFT", "days":7}' \
https://coorbital-hf-stock-predictor.hf.space/predict
```

## Notes
- replace `https://huggingface.co/` with `git@hf.co:` when clone the repo
    - check their doc on [SSH](https://huggingface.co/docs/hub/security-git-ssh)