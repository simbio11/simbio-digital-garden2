import { i18n } from "../i18n"
import { FullSlug, getFileExtension, joinSegments, pathToRoot } from "../util/path"
import { CSSResourceToStyleElement, JSResourceToScriptElement } from "../util/resources"
import { googleFontHref, googleFontSubsetHref } from "../util/theme"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { unescapeHTML } from "../util/escape"

export default (() => {
  const Head: QuartzComponent = ({
    cfg,
    fileData,
    externalResources,
    ctx,
  }: QuartzComponentProps) => {
    const titleSuffix = cfg.pageTitleSuffix ?? ""
    const title =
      (fileData.frontmatter?.title ?? i18n(cfg.locale).propertyDefaults.title) + titleSuffix
    const description =
      fileData.frontmatter?.socialDescription ??
      fileData.frontmatter?.description ??
      unescapeHTML(fileData.description?.trim() ?? i18n(cfg.locale).propertyDefaults.description)

    const { css, js, additionalHead } = externalResources

    const url = new URL(`https://${cfg.baseUrl ?? "example.com"}`)
    const path = url.pathname as FullSlug
    const baseDir = fileData.slug === "404" ? path : pathToRoot(fileData.slug!)
    const iconPath = joinSegments(baseDir, "static/icon.png")

    // Url of current page
    const socialUrl =
      fileData.slug === "404" ? url.toString() : joinSegments(url.toString(), fileData.slug!)

    const usesCustomOgImage = ctx.cfg.plugins.emitters.some((e) => e.name === "CustomOgImages")
    const ogImageDefaultPath = `https://${cfg.baseUrl}/static/og-image.png`

    const coreStylesheet = css[0]?.content
    const coreScript = js.find(
      (r) => r.loadTime === "beforeDOMReady" && r.contentType === "external",
    )

    return (
      <head>
        <title>{title}</title>
        <meta charSet="utf-8" />
        {coreStylesheet && <link rel="preload" href={coreStylesheet} as="style" />}
        {coreScript && coreScript.contentType === "external" && (
          <link rel="preload" href={coreScript.src} as="script" />
        )}
        {cfg.theme.cdnCaching && cfg.theme.fontOrigin === "googleFonts" && (
          <>
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" />
            <link rel="stylesheet" href={googleFontHref(cfg.theme)} />
            {cfg.theme.typography.title && (
              <link rel="stylesheet" href={googleFontSubsetHref(cfg.theme, cfg.pageTitle)} />
            )}
          </>
        )}
        <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossOrigin="anonymous" />
        <link rel="preconnect" href="https://cdn.jsdelivr.net" crossOrigin="anonymous" />
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />

        <meta name="og:site_name" content={cfg.pageTitle}></meta>
        <meta property="og:title" content={title} />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={title} />
        <meta name="twitter:description" content={description} />
        <meta property="og:description" content={description} />
        <meta property="og:image:alt" content={description} />

        {!usesCustomOgImage && (
          <>
            <meta property="og:image" content={ogImageDefaultPath} />
            <meta property="og:image:url" content={ogImageDefaultPath} />
            <meta name="twitter:image" content={ogImageDefaultPath} />
            <meta
              property="og:image:type"
              content={`image/${getFileExtension(ogImageDefaultPath) ?? "png"}`}
            />
          </>
        )}

        {cfg.baseUrl && (
          <>
            <meta property="twitter:domain" content={cfg.baseUrl}></meta>
            <meta property="og:url" content={socialUrl}></meta>
            <meta property="twitter:url" content={socialUrl}></meta>
          </>
        )}

        <link rel="icon" href={iconPath} />
        <meta name="description" content={description} />
        <meta name="generator" content="Quartz" />

        {css.map((resource) => CSSResourceToStyleElement(resource, true))}
        {js
          .filter((resource) => resource.loadTime === "beforeDOMReady")
          .map((res) => JSResourceToScriptElement(res, true))}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{if(!localStorage.getItem("theme")){document.documentElement.setAttribute("saved-theme","light")}}catch(e){}})();`,
          }}
        />
        {/* Simbio: 홈 인트로 워프는 세션 첫 방문에만 재생. 재방문·뒤로가기 시 html.sc-intro-seen 로 CSS 숨김 (헤드 스크립트는 매 nav 재실행 → 페인트 전에 클래스 세팅) */}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{if(sessionStorage.getItem("scIntroSeen")){document.documentElement.classList.add("sc-intro-seen");}else{sessionStorage.setItem("scIntroSeen","1");}}catch(e){}})();`,
          }}
        />
        {/* Simbio: 탐색기에서 상위 폴더를 접으면 하위 폴더도 모두 접히도록. MutationObserver 로 .folder-outer 의 open 제거를 감지 (explorer 의 stopPropagation 우회) */}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){if(window.__scFolderRecurse)return;window.__scFolderRecurse=1;function collapseKids(el){var subs=el.querySelectorAll(".folder-outer.open");if(!subs.length)return;var saved;try{saved=JSON.parse(localStorage.getItem("fileTree")||"[]")}catch(_){saved=[]}subs.forEach(function(s){s.classList.remove("open");var c=s.previousElementSibling,p=c&&c.dataset?c.dataset.folderpath:null;if(p){var i=saved.findIndex(function(x){return x.path===p});if(i>=0)saved[i].collapsed=true;else saved.push({path:p,collapsed:true})}});try{localStorage.setItem("fileTree",JSON.stringify(saved))}catch(_){}}var mo=new MutationObserver(function(muts){muts.forEach(function(m){var el=m.target;if(m.attributeName==="class"&&el.classList&&el.classList.contains("folder-outer")&&!el.classList.contains("open"))collapseKids(el)})});function wire(){document.querySelectorAll(".explorer-ul").forEach(function(u){mo.observe(u,{subtree:true,attributes:true,attributeFilter:["class"]})})}wire();document.addEventListener("nav",function(){setTimeout(wire,120)})})();`,
          }}
        />
        {/* Simbio: 정원 ↔ 인체 지도 공용 상단 스위치 + 테마 토글. 아틀라스와 마크업/동작 동일, ?sbcTheme 로 테마 동기화 */}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){var A="https://simbio-atlas.vercel.app/";function cur(){try{return document.documentElement.getAttribute("saved-theme")||localStorage.getItem("theme")||"light"}catch(e){return "light"}}try{var u=new URL(location.href),p=u.searchParams.get("sbcTheme");if(p==="dark"||p==="light"){document.documentElement.setAttribute("saved-theme",p);try{localStorage.setItem("theme",p)}catch(e){}var ap=function(){if(document.body){document.body.classList.remove("theme-dark","theme-light");document.body.classList.add("theme-"+p)}};ap();document.addEventListener("DOMContentLoaded",ap);u.searchParams.delete("sbcTheme");history.replaceState(null,"",u.pathname+u.search+u.hash)}}catch(e){}var M='<svg class="sbc-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',S='<svg class="sbc-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/></svg>';function mk(){if(document.querySelector(".sbc-switch")||!document.body)return;var n=document.createElement("nav");n.className="sbc-switch";n.setAttribute("aria-label","사이트 전환");n.innerHTML='<span class="sbc-switch-btn" data-active="true" aria-current="page"><span class="sbc-switch-dot"></span>코텍스</span><a class="sbc-switch-btn sbc-to-atlas" data-active="false" href="'+A+'"><span class="sbc-switch-dot"></span>인체 지도</a><button type="button" class="sbc-theme-toggle" aria-label="테마 전환" title="테마 전환">'+M+S+'</button>';document.body.appendChild(n);n.querySelector(".sbc-to-atlas").addEventListener("click",function(e){e.preventDefault();location.href=A+"?sbcTheme="+cur()});n.querySelector(".sbc-theme-toggle").addEventListener("click",function(){var d=document.querySelector(".darkmode");if(d){d.click()}else{var t=cur()==="dark"?"light":"dark";document.documentElement.setAttribute("saved-theme",t);try{localStorage.setItem("theme",t)}catch(e){}document.body.classList.remove("theme-dark","theme-light");document.body.classList.add("theme-"+t);document.dispatchEvent(new CustomEvent("themechange",{detail:{theme:t}}))}})}mk();document.addEventListener("DOMContentLoaded",mk);document.addEventListener("nav",function(){setTimeout(mk,0)})})();`,
          }}
        />
        {additionalHead.map((resource) => {
          if (typeof resource === "function") {
            return resource(fileData)
          } else {
            return resource
          }
        })}
      </head>
    )
  }

  return Head
}) satisfies QuartzComponentConstructor
