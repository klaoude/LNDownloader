#SingleInstance force

WinActivate, DeepL Pro
MouseClick, left, 300, 300
Sleep 150
MouseClick, left, 300, 300
Sleep 150
Send ^a
Sleep 150
Send ^v
Sleep 10000
Clipboard := ""
targetcolor := 0x006494
WinActivate, DeepL Pro
PixelGetColor, color, 499, 523, RGB
while color = targetcolor
{
    Sleep 500
    WinActivate, DeepL Pro
    PixelGetColor, color, 499, 523, RGB
}
Sleep 200
WinActivate, DeepL Pro
MouseClick, left, 800, 300
Sleep 150
MouseClick, left, 800, 300
Sleep 150
Send ^a
Sleep 150
Send ^c
Sleep 200