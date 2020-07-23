class DeepLTranslator {
	
	static formatURL := "https://www.deepl.com/en/translator#{2:s}/{3:s}/{1:s}"

	__New() {
		this.IE := ComObjCreate("InternetExplorer.Application") 
	}

	__Delete() {
		this.IE.Quit
	}
	translate(sourceText, languageOut, languageIn := "auto") {
		sourceURL := this.uriEncode(sourceText)
		url := Format(This.formatURL, sourceURL, languageIn, languageOut)
		this.navigate(url)
		return this.translation() 
	}
	
	navigate(url) {
		this.IE.Navigate(url)
		While (this.IE.readyState != 4 || this.IE.document.readyState != "complete" || this.IE.busy)
			Sleep 50
	}
	
	translation() {
		While ((result := this.IE.document.getElementsByTagName("textarea")[1].value) = "")
			Sleep 50
		return result
	}
	
	uriEncode(sourceText) {
		return StrReplace(sourceText, " ", "%20")
	}
}

translator := new DeepLTranslator()
!d::
Send ^c
Clipboard := translator.translate(Clipboard, "en", "fr")