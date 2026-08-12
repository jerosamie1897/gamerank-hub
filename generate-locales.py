from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE = "https://gamerankhub.com"

LOCALES = {
    "zh-cn": {
        "lang": "zh-CN",
        "dir": "ltr",
        "name": "简体中文",
        "title": "GameRank Hub 中文版：游戏评测与实用攻略",
        "description": "浏览免费游戏评测、新手攻略、平台比较、付费模式说明以及适合不同设备和游戏时间的推荐。",
        "eyebrow": "中文游戏指南",
        "heading": "更清楚地选择游戏，更安心地开始游玩",
        "lede": "GameRank Hub 通过清晰的比较、可见的更新时间和实用的新手建议，帮助玩家了解游戏是否适合自己的设备、预算、时间和游玩方式。",
        "sections": [
            ("如何使用本站", "先从游戏评测了解平台、类型、单局时间、核心玩法和付费模式，再阅读设置、性能、团队沟通与安全方面的攻略。详细评测目前以英文发布，本中文入口提供结构化导航和关键说明。"),
            ("评测关注什么", "我们的评测不会只根据热度排名。我们关注新手引导是否清楚、普通玩家能否理解目标、免费内容是否完整、可选购买是否透明、性能是否稳定，以及无障碍设置能否满足不同玩家的需要。"),
            ("免费游戏与消费安全", "免费游玩并不代表所有内容都免费。开始消费前，请确认购买的是外观、便利功能、扩展内容还是随机奖励。为账户启用购买验证，并提前设定娱乐预算。"),
            ("社区与更新", "每个游戏评测页面都支持玩家评分和经过审核的评论。重要的内容、技术和社区更新会记录在更新日志中，RSS 订阅可用于跟踪新文章。"),
        ],
        "reviews": "查看游戏评测",
        "guides": "阅读实用攻略",
        "community": "访问玩家社区",
        "languages": "其他语言",
    },
    "ja": {
        "lang": "ja",
        "dir": "ltr",
        "name": "日本語",
        "title": "GameRank Hub 日本語：ゲームレビューと実用ガイド",
        "description": "基本プレイ無料ゲームのレビュー、初心者向けガイド、対応機種、課金方式、プレイ時間、安全設定を分かりやすく比較します。",
        "eyebrow": "日本語ゲームガイド",
        "heading": "自分の時間、端末、遊び方に合うゲームを見つける",
        "lede": "GameRank Hub は、誇張よりも判断材料を重視します。対応プラットフォーム、1回のプレイ時間、初心者向けの分かりやすさ、課金、アクセシビリティを整理して紹介します。",
        "sections": [
            ("サイトの使い方", "まずレビューでゲームの目的、対応機種、セッション時間、主な長所と注意点を確認してください。その後、操作設定、パフォーマンス、チーム連携、安全な課金に関するガイドを利用できます。詳細記事は現在英語ですが、このページから主要な情報へ移動できます。"),
            ("レビュー方針", "人気だけで順位を決めません。チュートリアルの質、通常プレイで生まれる判断、進行システム、価格の透明性、安定性、アクセシビリティ、長期的な負担を確認します。変更されやすい情報は公式サイトでも確認してください。"),
            ("無料ゲームを安全に楽しむ", "購入前に、商品が外見アイテム、追加コンテンツ、時間短縮、ランダム報酬のどれに当たるかを確認しましょう。購入認証を有効にし、期間限定表示に急かされず、先に予算を決めることを推奨します。"),
            ("コミュニティと更新", "各レビューではプレイヤー評価を送信でき、コメントは公開前にモデレーションされます。大きな編集変更や技術更新は更新ログに記録されます。"),
        ],
        "reviews": "ゲームレビューを見る",
        "guides": "実用ガイドを読む",
        "community": "コミュニティを見る",
        "languages": "ほかの言語",
    },
    "ko": {
        "lang": "ko",
        "dir": "ltr",
        "name": "한국어",
        "title": "GameRank Hub 한국어: 게임 리뷰와 실용 가이드",
        "description": "무료 게임 리뷰, 초보자 가이드, 지원 플랫폼, 플레이 시간, 과금 방식, 성능과 안전 설정을 명확하게 비교합니다.",
        "eyebrow": "한국어 게임 가이드",
        "heading": "시간과 기기, 플레이 방식에 맞는 게임을 선택하세요",
        "lede": "GameRank Hub는 과장된 순위보다 실제 선택에 필요한 정보를 제공합니다. 플랫폼, 세션 길이, 진입 장벽, 선택 구매, 접근성 및 성능을 쉽게 확인할 수 있습니다.",
        "sections": [
            ("사이트 이용 방법", "게임 리뷰에서 장르, 플랫폼, 평균 세션 시간, 핵심 플레이와 초보자 계획을 먼저 확인하세요. 이후 조작 설정, 프레임 안정성, 팀 소통, 크로스플레이와 안전한 결제에 관한 가이드를 참고할 수 있습니다. 상세 리뷰는 현재 영어로 제공됩니다."),
            ("리뷰 기준", "인기만으로 게임을 추천하지 않습니다. 목표가 명확한지, 첫 10회 플레이가 이해하기 쉬운지, 무료 콘텐츠가 충분한지, 과금이 투명한지, 성능과 접근성 옵션이 실제로 도움이 되는지 평가합니다."),
            ("무료 게임과 결제 안전", "구매 항목이 스킨, 편의 기능, 확장 콘텐츠, 무작위 보상 중 무엇인지 확인하세요. 플랫폼 구매 인증을 켜고 예산을 미리 정하면 기간 한정 판매나 반복 결제로 인한 충동 지출을 줄일 수 있습니다."),
            ("커뮤니티와 업데이트", "모든 리뷰 페이지에서 플레이어 평점을 남길 수 있습니다. 댓글은 스팸과 악용을 줄이기 위해 검토 후 공개되며, 중요한 사이트 변경은 업데이트 로그와 RSS에 기록됩니다."),
        ],
        "reviews": "게임 리뷰 보기",
        "guides": "실용 가이드 읽기",
        "community": "플레이어 커뮤니티",
        "languages": "다른 언어",
    },
    "ar": {
        "lang": "ar",
        "dir": "rtl",
        "name": "العربية",
        "title": "GameRank Hub بالعربية: مراجعات ألعاب وأدلة عملية",
        "description": "قارن مراجعات الألعاب المجانية والمنصات ومدة الجلسة ونظام المشتريات وإعدادات الأداء والأمان قبل بدء اللعب.",
        "eyebrow": "دليل الألعاب باللغة العربية",
        "heading": "اختر لعبة تناسب وقتك وجهازك وطريقة لعبك",
        "lede": "يوفر GameRank Hub معلومات واضحة تساعدك على اتخاذ القرار، بما في ذلك المنصات المدعومة ومدة الجلسة وسهولة البداية والمشتريات الاختيارية وإمكانية الوصول والأداء.",
        "sections": [
            ("طريقة استخدام الموقع", "ابدأ بصفحة المراجعات لمعرفة نوع اللعبة والمنصات ومدة الجلسة وأهم المزايا والقيود. بعد ذلك استخدم الأدلة العملية لضبط التحكم وتحسين ثبات الأداء وفهم اللعب الجماعي واللعب المشترك والإنفاق الآمن. المقالات التفصيلية متاحة حالياً باللغة الإنجليزية."),
            ("منهجية المراجعة", "لا نعتمد على الشهرة وحدها. ننظر إلى وضوح الشرح للمبتدئ وجودة القرارات أثناء اللعب وسهولة الوصول إلى المحتوى المجاني وشفافية الأسعار والأداء وخيارات إمكانية الوصول والوقت المطلوب للتقدم."),
            ("الألعاب المجانية والشراء الآمن", "تحقق مما إذا كانت المشتريات تمنح عناصر تجميلية أو محتوى إضافياً أو اختصاراً للوقت أو مكافآت عشوائية. فعّل تأكيد الشراء وحدد ميزانية ترفيهية مسبقاً ولا تسمح للعروض المحدودة زمنياً بالضغط عليك."),
            ("المجتمع والتحديثات", "يمكن للاعبين إضافة تقييم لكل مراجعة، وتخضع التعليقات للمراجعة قبل النشر للحد من الرسائل المزعجة والإساءة. نسجل التغييرات المهمة في سجل تحديثات واضح ونوفر موجز RSS."),
        ],
        "reviews": "عرض مراجعات الألعاب",
        "guides": "قراءة الأدلة العملية",
        "community": "زيارة مجتمع اللاعبين",
        "languages": "لغات أخرى",
    },
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def alternates() -> str:
    links = ['  <link rel="alternate" hreflang="x-default" href="https://gamerankhub.com/">', '  <link rel="alternate" hreflang="en" href="https://gamerankhub.com/">']
    links.extend(f'  <link rel="alternate" hreflang="{data["lang"]}" href="{BASE}/{slug}/">' for slug, data in LOCALES.items())
    return "\n".join(links)


def render(slug: str, data: dict[str, object]) -> str:
    cards = "".join(f"<article><h2>{esc(title)}</h2><p>{esc(body)}</p></article>" for title, body in data["sections"])
    language_links = "".join(f'<a href="../{code}/" hreflang="{locale["lang"]}">{esc(locale["name"])}</a>' for code, locale in LOCALES.items() if code != slug)
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": data["title"],
        "description": data["description"],
        "url": f"{BASE}/{slug}/",
        "inLanguage": data["lang"],
        "isPartOf": {"@type": "WebSite", "name": "GameRank Hub", "url": f"{BASE}/"},
    }
    return f"""<!doctype html>
<html lang="{data["lang"]}" dir="{data["dir"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(data["title"])}</title>
  <meta name="description" content="{esc(data["description"])}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{BASE}/{slug}/">
{alternates()}
  <link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../assets/styles.css?v=20260812-5">
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header"><div class="shell nav-wrap"><a class="brand" href="../index.html"><span class="brand-mark">G</span><span>GameRank <strong>Hub</strong></span></a><nav class="site-nav"><a href="../reviews/index.html">{esc(data["reviews"])}</a><a href="../guides/index.html">{esc(data["guides"])}</a><a href="../community.html">{esc(data["community"])}</a></nav></div></header>
  <main id="main">
    <section class="article-hero purple-hero"><div class="shell narrow"><p class="eyebrow">{esc(data["eyebrow"])}</p><h1>{esc(data["heading"])}</h1><p class="hero-lede">{esc(data["lede"])}</p><div class="hero-actions"><a class="button button-primary" href="../reviews/index.html">{esc(data["reviews"])}</a><a class="button button-ghost" href="../guides/index.html">{esc(data["guides"])}</a></div></div></section>
    <section class="section shell"><div class="library-grid">{cards}</div></section>
    <section class="section shell"><p class="eyebrow">{esc(data["languages"])}</p><div class="language-grid"><a href="../" hreflang="en">English</a>{language_links}</div></section>
  </main>
  <footer class="site-footer"><div class="shell footer-bottom"><span>© <span data-year>2026</span> GameRank Hub</span><a href="../updates.html">Updates</a><span data-credit>Designed &amp; Developed by JTB</span></div></footer><script src="../assets/script.js?v=20260812-6" defer></script>
</body>
</html>"""


for slug, locale in LOCALES.items():
    destination = ROOT / slug / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render(slug, locale), encoding="utf-8", newline="\n")

print(f"Generated {len(LOCALES)} localized hubs.")
