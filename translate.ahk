#SingleInstance force

!d::

Send ^c
Clipboard := DeeplTranslate(Clipboard, "en", "fr")

DeeplTranslate(Source,LangIn,LangOut)
{
    StringReplace, Source, Source, %A_Space%, `%20, All  ;you don't need this, but you can keep it in
    Base := "https://www.deepl.com/en/translator#"
    Path := Base . LangIn . "/" . LangOut . "/" . Source
    IE := ComObjCreate("Shell.Application") ;~ Creation of hidden Internet Explorer instance to look up Google Translate and retrieve translation
    IE.Open(Path)
    While IE.readyState!=4 || IE.document.readyState!="complete" || IE.busy
        Sleep 50
	While (IE.document.getElementsByTagName("textarea")[1].value = "")  ;Since the conversion takes a second we want to wait till the value is filled otherwise the return will always be nothing
		Sleep 50
    Result := IE.document.getElementsByTagName("textarea")[1].value
    IE.Quit
    Return Result
}