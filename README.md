# Linux Browser Selector
Choose your web browser for links in any app on Linux, and remember your choice if needed. Customize the browsers (or apps) you want to use.
<br><br>



<br><br>


## Description
Whenever you click on a link (or web-related file), you can choose which web browser shall be used to open it.
<br>
It is basically a replacement of your default web browser in the first place, so you can use it to subsequently call and run different browsers instead, e.g. one for anonymous surfing, one for online accounts, one for secure banking, another one for coding, testing and so on.
<br>
The script is a combination of the functions from [Junction](https://github.com/sonnyp/Junction) on Linux -- much like [Choosy](https://www.choosyosx.com/) on Mac, or [BrowseRouter](https://github.com/slater1/BrowseRouter) on Win.

## Installation
### ToDo till 29. Aug 2024:
* Download (and extract) or clone the repo (see buttons above on the right hand side)
* run the .sh file in `install/` to install all dependencies (like Python 2 and Qt 4)
    * `cd install && chmod +x *.sh`
    * `./browserSelectorInstall.sh`
* change `browserSelectorInstall.py` file in `source/` to reflect your setup and needs
    * make sure all your referenced browser `.desktop` files use an uppercase `%U` at the end of the `Exec` line
* test it e.g. with `./browserSelector.py https://gitlab.com`, or `./browserSelector.py ../tests/ab.html`

## Default Config
* change `browserSelector.desktop` file in `install/` as needed on your system
    * and copy it to your appropriate path (e.g. `~/.local/share/applications/`)
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

## Known Issues
In case your browser doesn't open, its process may hang for some reason -- then simply check and kill it, e.g. with `ps -fe | grep chrome` and `pkill -9 chrome`

## Support
Please try a [Search](https://presearch.com/) first, then post your Issue -- maybe someone can help you. I'm just a hobby coder 😊

## License
MIT

## Status
* Release: testing
