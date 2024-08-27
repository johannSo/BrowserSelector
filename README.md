# Linux Browser Selector
Choose your web browser for links in any app on Linux, and remember your choice if needed. Customize the browsers (or apps) you want to use.
<br><br>
![](images/screenshot.png)
<br>
Above, a link to GitLab is opened, and five browser options have been configured.

## Description
Whenever you click on a link (or web-related file), you can choose which web browser shall be used to open it. By clicking the RMBR checkbox, the script will remember your choice for the next time for this particular domain or file, so the script works silently in the background.
<br>
It is basically a replacement of your default web browser in the first place, so you can use it to subsequently call and run different browsers instead, e.g. one for anonymous surfing, one for online accounts, one for secure banking, another one for coding, testing and so on.
<br>
The script is a combination of the functions from [Junction](https://github.com/sonnyp/Junction) on Linux -- much like [Choosy](https://www.choosyosx.com/) on Mac, or [BrowseRouter](https://github.com/slater1/BrowseRouter) on Win.

## Installation
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

## Usage
* just click a link (or file) in any app and then choose your browser, right where your mouse pointer is -- **Enjoy**!
    * beside using the mouse you can also use your left/right cursor keys and the space key to open your browser
* edit the `.json` in `source/` if you want to change the remembered domains or files
    * you don't need to add multiple entries for (or w/o) `www`, or for protocols like `http`/`https` etc. -- domain and top-level is enough (e.g. just `gitlab.com`)
    * ports are treated like different domains (e.g. `localhost:8080` is different to `localhost`)
    * pathes in URLs and files are generally ignored on purpose

## Known Issues
In case your browser doesn't open, its process may hang for some reason -- then simply check and kill it, e.g. with `ps -fe | grep chrome` and `pkill -9 chrome`

## Support
Please try a [Search](https://presearch.com/) first, then post your Issue -- maybe someone can help you. I'm just a hobby coder 😊

## Roadmap
Nothing planned so far

## Contributing
First idea and implementation is from AiwendilH @ [Reddit](https://www.reddit.com/r/linux/comments/2lgokr/looking_for_an_app_that_lets_you_choose_web/)
<br>
Forks or Merge requests are welcome!

## License
MIT

## Status
* Release: stable
* The fork https://gitlab.com/nucleware/browserselector got some major improvements, beside others:
    * support of Python 3 and Qt6
    * bugfix of [issue #1](https://gitlab.com/ToS0/browserselector/-/issues/1)
    * auto-config of web browsers
