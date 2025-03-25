---
layout: splash
permalink: /
title: planetoids
header:
  overlay_image: /images/planetoids.gif
  cta_label: "<i class='fa fa-download'></i> pip install planetoids-game"
  cta_url: "https://pypi.org/project/planetoids-game"
excerpt: Retro-inspired arcade space shooter

feature_row:
  - image_path: images/red.PNG
    image_size: 100px
    alt: ""
    title: ""
    excerpt: ""
    url: ""
    btn_label: "Learn More"
  - image_path: images/green.PNG
    alt: ""
    title: ""
    excerpt: ""
    url: ""
    btn_label: "Learn More"
  - image_path: images/blue.PNG
    alt: "100% free"
    title: ""
    excerpt: ""
    url: "/license/"
    btn_label: "Learn More"
github:
  - excerpt: '{::nomarkdown}<iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=mmistakes&repo=minimal-mistakes&type=star&count=true&size=large" frameborder="0" scrolling="0" width="160px" height="30px"></iframe> <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=mmistakes&repo=minimal-mistakes&type=fork&count=true&size=large" frameborder="0" scrolling="0" width="158px" height="30px"></iframe>{:/nomarkdown}'
---

{% include feature_row %}

<p align="center">
  <img src="https://github.com/chris-greening/spyrograph/blob/gh-pages/images/circle_spinning.gif?raw=true" alt="Sample hypotrochoid drawing showing a circle rolling around the interior of another circle drawing a geometric shape" width="410px">
</p>

<h2> Recent Blog Posts </h2>

{% for post in site.posts limit:3 %}
  {% include archive-single.html %}
{% endfor %}

[See all blog posts...]({{site.url}}{{site.baseurl}}/blog/){: .btn .btn--info}