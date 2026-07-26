# 대표 이미지 수동 오버라이드

`archive-thumbs.py` 는 각 페이지에 임베드된 가장 큰 이미지를 대표 이미지로 뽑아
격자 썸네일(`p/archive/thumbs/<slug>.webp`)과 공유 미리보기(`og/<slug>.jpg`)를 굽는다.
자동 추출 결과가 부적절하거나 본문에 삽화가 없는 글은 여기에 파일을 두면 그것을 쓴다.

```
backlog/assets/page-image-override/<slug>.webp   (또는 .png / .jpg / .jpeg)
```

- 슬러그는 루트 `index.html` 카드의 `href` 마지막 세그먼트다.
- 썸네일·OG 공통 훅이다. 둘을 따로 지정할 수는 없다.
- 원본 해상도는 크게 둔다. 1200x630 으로 채워 자르므로 가로 1200px 이상을 권한다.
- 파일을 두거나 지운 뒤에는 `archive-thumbs.py` → `relink-pages.py` 순으로 다시 돌린다.
