# Linux Browser Selector
Choose your web browser for links in any app on Linux, and remember your choice if needed. Customize the browsers (or apps) you want to use.
<br><br>

![](https://github.com/johannSo/GTK-Browser_Selector/blob/main/images/v2.4.png?raw=true)

<br><br>


## Description
Whenever you click on a link (or web-related file), you can choose which web browser shall be used to open it.
<br>
It is basically a replacement of your default web browser in the first place, so you can use it to subsequently call and run different browsers instead, e.g. one for anonymous surfing, one for online accounts, one for secure banking, another one for coding, testing and so on.
<br>
The script is a combination of the functions from [Junction](https://github.com/sonnyp/Junction) on Linux -- much like [Choosy](https://www.choosyosx.com/) on Mac, or [BrowseRouter](https://github.com/slater1/BrowseRouter) on Win.

## Installation
* Download (and extract) or clone the repo (see buttons above on the right hand side)
* run the .sh file in `install/` to install all dependencies (like Python 3 and GTK 4)
    * `cd install && chmod +x *.sh`
    * `./browserSelectorInstall.sh`
* change `browserSelectorInstall.py` file in `source/` to reflect your setup and needs
    * make sure all your referenced browser `.desktop` files use an uppercase `%U` at the end of the `Exec` line
* test it e.g. with `./browserSelector.py https://gitlab.com`, or `./browserSelector.py ../tests/ab.html`

## Default Config
*To use your own Browsers in the Selector you hav to add your execution command in the source/gui.py file! (I'am working on an automatic version)
* add `browserSelector.desktop` to the following protocol entries in `~/.config/mimeapps.list`:
    * in section `[Default Applications]` to (separated by semicolon)
        * `text/html`
        * `text/xml`
        * `image/webp`
        * `x-scheme-handler/http`
        * `x-scheme-handler/https`
        * `x-scheme-handler/ftp`
        * `application/xhtml_xml`
    * and do it all over again for the same entries in `[Added Associations]` further down the file
        * so, for example, you have twice something like this in your file: `text/html=codium.desktop;browserSelector.desktop;`
* now logout from your desktop session and login again to have your changes loaded
* finally link your Default web browser setting to `Browser Selector`
    * in Gnome: `System settings` / `Default applications` / `Web`
    * in KDE: `Settings` / `Standard Components`
    * you may also run `xdg-settings set default-web-browser browserSelector.desktop` from your shell instead
* test it e.g. with `xdg-open https://gitlab.com`, or `xdg-open ../tests/ab.html`

## Support
If you find an bug you can open an Issue page on Github but I dont know if i can responde to it, please try a search first!

## ToDo:
- Make an automatic script to find and implement Browsers in the selector

## License
MIT

## Status
* Release: stable <br>
Status: In activ Development

## Idea:
Original idea by [ToSo](https://gitlab.com/ToS0/browserselector/)


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=johannSo/GTK-Browser_Selector&type=Date)](https://star-history.com/#johannSo/GTK-Browser_Selector&Date)
