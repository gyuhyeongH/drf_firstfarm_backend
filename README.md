# 첫농
- 농사 체험/근로 중개 서비스 첫농 입니다.
- [기획서](https://www.notion.so/02991c731e82421abd2af57895737edb)

<br>

<img src="https://user-images.githubusercontent.com/104343834/186075393-9166da84-badb-4b08-ae5c-5e34b7a059ad.png" width="400">

# 1. 제작 기간 & 참여 인원
- 22.07.07 ~ 22.08.16 (6주)
- 백엔드 개발자 4명

<br>

# 2. 사용 기술
  - Python
  - Django 4.0
  - DRF
  - Docker
  - AWS EC2
  - Nginx
  - Gunicorn
  - S3
  - JavaScript
  - HTML/CSS

<br>

# 3. ERD 설계

![ERD_첫농](https://user-images.githubusercontent.com/104343834/186077962-316059fe-8bb1-4492-bb7e-b270f7dbb3ea.png)

<br>

# 4. 핵심 기능
첫농 핵심기능

<details>
<summary>핵심 기능 설명 펼치기</summary>
<div markdown="1">       

- 공고 신청 ✅ [코드 확인](https://github.com/HWISU96-Portfolio/Firstfarm_backend/blob/6f9fcadee634c3e98aa285c68344ef972b97e55f/article/views.py#L199-L212)  
  - 해당 article_id 와 현재 user 신청기록 DB에 저장  
  
  
- 지원자 선발 ✅ [코드 확인](https://github.com/HWISU96-Portfolio/Firstfarm_backend/blob/6f9fcadee634c3e98aa285c68344ef972b97e55f/article/views.py#L256-L274)  
  - 자신이 올린 공고중 특정 공고에 지원한 신청자 조회 및 선발
  
- 공고 마감 ✅ [코드 확인](https://github.com/HWISU96-Portfolio/Firstfarm_backend/blob/6f9fcadee634c3e98aa285c68344ef972b97e55f/article/views.py#L188-L196)  
  - 선발 완료한 공고 마감
  
</div>
</details>

<br>

# 5.  트러블 슈팅

<details>
<summary>XSS</summary>
<div markdown="1">       

배포 직후 반사형 XSS 공격이 들어와 브라우저에서 악성 스크립트가 실행되는 문제 발생  
→ Javascript에서 정규표현식으로 치환하여 기초적인 방어 기능 구현  
→ 라이브러리 (lucy-xss-servlet-filter) 사용을 통한 XSS 취약점 보완 방법 탐색
  
✅ [코드 확인](https://github.com/gyuhyeongH/firstfarm_front2/blob/837f7e5cefe37222e1d0ba248ad556e61de9d9c5/js/articleupload.js#L1-L9)
</div>
</details>

<br>

<details>
<summary>상세 게시물 탐색 문제</summary>
<div markdown="1">       

여러 게시물들 중 특정 게시물을 클릭했을때, 해당하는 경로를 제대로 지정하지 못하는 문제 발생  
→ 클릭한 게시물의 article_id 값을 사용하기 위해 로컬 스토리지에 데이터를 저장하여 전달

  
✅ [코드 확인](https://github.com/gyuhyeongH/firstfarm_front2/blob/837f7e5cefe37222e1d0ba248ad556e61de9d9c5/js/articledetail.js#L1-L4)
</div>
</details>
<br>

<details>
<summary>mecab 윈도우 호환 문제</summary>
<div markdown="1">       

mecab 라이브러리가 window에서는 사용 불가능하여 배포 전 테스트하는데 어려움 발생  
→ 도커를 이용하여 해결

  
✅ [코드 확인](https://github.com/gyuhyeongH/drf_firstfarm_backend/blob/16397b02c76d13ff8ef200633b63256f2a326658/Dockerfile#L1)
</div>
</details>


