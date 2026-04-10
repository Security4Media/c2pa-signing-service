function isPrivateHost(hostname) {
  if (!hostname) {
    return true
  }

  const normalized = hostname.toLowerCase()

  if (
    normalized === "localhost" ||
    normalized === "0.0.0.0" ||
    normalized === "::1" ||
    normalized === "[::1]"
  ) {
    return true
  }

  if (/^127\.\d+\.\d+\.\d+$/.test(normalized)) {
    return true
  }

  if (/^10\.\d+\.\d+\.\d+$/.test(normalized)) {
    return true
  }

  if (/^192\.168\.\d+\.\d+$/.test(normalized)) {
    return true
  }

  const const172 = normalized.match(/^172\.(\d+)\.\d+\.\d+$/)
  if (const172) {
    const secondOctet = Number.parseInt(const172[1], 10)
    if (secondOctet >= 16 && secondOctet <= 31) {
      return true
    }
  }

  return false
}

function initOpenApiViewerLinks() {
  const links = document.querySelectorAll("[data-openapi-viewer-link]")

  links.forEach((link) => {
    if (!(link instanceof HTMLAnchorElement)) {
      return
    }

    const defaultHref = "https://editor.swagger.io/"
    const specPath = link.dataset.openapiSpecPath || "api/openapi.json"
    const { protocol, hostname } = window.location
    const specUrl = new URL(specPath, window.location.href)
    const eyebrow = link.querySelector(".brand-card__eyebrow")
    const title = link.querySelector(".brand-card__title")
    const copy = link.querySelector(".brand-card__copy")

    function setCardText(mode) {
      const eyebrowText = link.dataset[`${mode}Eyebrow`]
      const titleText = link.dataset[`${mode}Title`]
      const copyText = link.dataset[`${mode}Copy`]

      if (eyebrow && eyebrowText) {
        eyebrow.textContent = eyebrowText
      }

      if (title && titleText) {
        title.textContent = titleText
      }

      if (copy && copyText) {
        copy.textContent = copyText
      }
    }

    if (protocol === "file:" || isPrivateHost(hostname)) {
      link.href = specUrl.toString()
      link.removeAttribute("target")
      link.removeAttribute("rel")
      link.title = "Open the generated OpenAPI JSON from this docs site."
      setCardText("private")
      return
    }

    link.href = `${defaultHref}?url=${encodeURIComponent(specUrl.toString())}`
    link.target = "_blank"
    link.rel = "noopener noreferrer"
    link.title = "Open the generated OpenAPI spec in Swagger Editor."
    setCardText("public")
  })
}

document$.subscribe(initOpenApiViewerLinks)
