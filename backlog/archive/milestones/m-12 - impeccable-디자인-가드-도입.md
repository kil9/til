---
id: m-12
title: "impeccable 디자인 가드 도입"
---

## Description

AI 디자인 가드 도구 impeccable(pbakaus/impeccable, Apache 2.0)을 프로젝트 로컬로 도입한다. 각 페이지가 자체 완결형 HTML 로 매번 새로 생성되는 구조라 페이지 간 디자인 일관성이 실제 페인 포인트이고, DESIGN.md 로 리브 투데이 사이트의 디자인 언어를 고정하는 것이 핵심 가치다. 주의: main 루트가 GitHub Pages 로 그대로 서빙되므로 잡파일이 공개 서빙되지 않게 gitignore 를 챙긴다. 훅은 API 호출 없는 로컬 node 스크립트라 토큰 비용이 없다.
