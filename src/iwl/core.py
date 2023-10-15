import yaml
from .exceptions import *


class Engine:
    @staticmethod
    def convert(code: str): ...


class BaseEngine(Engine):
    __html_kw = {"type": "", "text": "", "styl": "", "style": "",
                 "href": "href", "sour": "src", "source": "scr",
                 "valu": "value", "value": "value"}

    __type_kw = {"button": "button", "box": "div", "label": "label", "span": "span",
                 "canvas": "canvas", "image": "img", "entry": "input", "link": "a",
                 "list": "li", "table": "table", "media": "source", "svg": "svg",
                 "video": "video", "multiline_entry": "textarea"}

    @staticmethod
    def __safe_split(input_string):
        input_string = input_string.lstrip("​")
        split_parts = []
        current_part = ''
        inside_parentheses = False

        for char in input_string:
            if char == ' ' and not inside_parentheses:
                if current_part:
                    split_parts.append(current_part)
                current_part = ''
            else:
                current_part += char
                if char == '(':
                    inside_parentheses = True
                elif char == ')':
                    inside_parentheses = False

        if current_part:
            split_parts.append(current_part)

        return split_parts

    @staticmethod
    def convert(code: str):
        while True:
            if "include" in code:
                path = code.split('include ')[1].split('\n')[0]
                indent = code.split("include")[0].splitlines()[-1]
                include = "\n".join(indent + line for line in open(path, "r").read().splitlines())
                code = code.replace(indent + 'include ' + path, include, 1)
            else:
                break

        code = code.replace(": -", ": ​-")

        try:
            data: dict = yaml.safe_load(code)
        except:
            raise SyntaxError("Exception while parsing the iwl converted yaml file.")

        script = data.get("_script", None)
        objects = data.get("_objects", None)
        structure = data.get("_structure", None)
        animations = data.get("_animations", None)

        obj_htmls = ""

        if objects:
            obj_htmls = BaseEngine.__load_objects(objects)

        return "<style>\n" + BaseEngine.__parse_animations(animations) + \
            "\n.active:active {animation: var(--active)}\n.any-link:any-link {animation: var(--any-link)}" \
            "\n.autofill:autofill {animation: var(--autofill)}\n.checked:checked {animation: var(--checked)}" \
            "\n.default:default {animation: var(--default)}\n.defined:defined {animation: var(--defined)}" \
            "\n.disabled:disabled {animation: var(--disabled)}\n.empty:empty {animation: var(--empty)}" \
            "\n.enabled:enabled {animation: var(--enabled)}\n.first:first {animation: var(--first)}" \
            "\n.first-child:first-child {animation: var(--first-child)}" \
            "\n.first-of-type:first-of-type {animation: var(--first-of-type)}" \
            "\n.fullscreen:fullscreen {animation: var(--fullscreen)}\n.focus:focus {animation: var(--focus)}" \
            "\n.focus-visible:focus-visible {animation: var(--focus-visible)}" \
            "\n.focus-within:focus-within {animation: var(--focus-within)}\n.host:host {animation: var(--host)}" \
            "\n.hover:hover {animation: var(--hover)}\n.indeterminate:indeterminate {animation: var(--indeterminate)}" \
            "\n.in-range:in-range {animation: var(--in-range)}\n.invalid:invalid {animation: var(--invalid)}" \
            "\n.last-child:last-child {animation: var(--last-child)}" \
            "\n.last-of-type:last-of-type {animation: var(--last-of-type)}\n.left:left {animation: var(--left)}" \
            "\n.link:link {animation: var(--link)}\n.modal:modal {animation: var(--modal)}" \
            "\n.only-child:only-child {animation: var(--only-child)}" \
            "\n.only-of-type:only-of-type {animation: var(--only-of-type)}" \
            "\n.optional:optional {animation: var(--optional)}" \
            "\n.out-of-range:out-of-range {animation: var(--out-of-range)}" \
            "\n.picture-in-picture:picture-in-picture {animation: var(--picture-in-picture)}" \
            "\n.placeholder-shown:placeholder-shown {animation: var(--placeholder-shown)}" \
            "\n.paused:paused {animation: var(--paused)}\n.playing:playing {animation: var(--playing)}" \
            "\n.read-only:read-only {animation: var(--read-only)}" \
            "\n.read-write:read-write {animation: var(--read-write)}\n.required:required {animation: var(--required)}" \
            "\n.right:right {animation: var(--right)}\n.root:root {animation: var(--root)}" \
            "\n.scope:scope {animation: var(--scope)}\n.target:target {animation: var(--target)}" \
            "\n.valid:valid {animation: var(--valid)}\n.visited:visited {animation: var(--visited)}\n</style>" + \
            BaseEngine.__arrange_objects(obj_htmls, structure) + (f"<script>{script}</script>" if script else "")

    @staticmethod
    def __css_from_attr(key, attr):
        match key:
            case "anim" | "animation":  # anim: name duration timing-function delay iteration-count direction play-state
                style = ""
                classes = ""
                for arg in attr:
                    match arg:
                        case "default":
                            style += f"animation: {attr[arg]}; "
                        case _:
                            style += f"--{arg}: {attr[arg]}; "
                            classes += f"{arg} "
                return style, classes

            case "back" | "background":  # back: color img-src|url("...") position size attach repeat|(x y)/both\none
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"background-color: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"background-image: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                    if len(attr_spl) > 2:
                        style += f"background-attachment: {attr_spl[2]}; " if attr_spl[2] != "-" else ""
                        if len(attr_spl) > 3:
                            style += f"background-repeat: " \
                                     f"{attr_spl[3].replace('x', 'repeat-x').replace('y', 'repeat-y').replace('both', 'repeat').replace('none', 'no-repeat')}; " \
                                if attr_spl[3] != "-" else ""
                            if len(attr_spl) > 4:
                                style += f"background-position: {attr_spl[4].replace('(', '').replace(')', '')}; " \
                                    if attr_spl[4] != "-" else ""
                                if len(attr_spl) > 5:
                                    style += f"background-size: {attr_spl[5].replace('(', '').replace(')', '')}; " \
                                        if attr_spl[5] != "-" else ""
                return style, None

            case "bord" | "border":
                style = ""
                for arg in attr:
                    match arg:
                        case "n" | "nort" | "north":  # n: width style color
                            style += f"border-top: {attr[arg]}; " if attr[arg] != "-" else ""

                        case "e" | "east":  # e: width style color
                            style += f"border-right: {attr[arg]}; " if attr[arg] != "-" else ""

                        case "s" | "sout" | "south":  # s: width style color
                            style += f"border-bottom: {attr[arg]}; " if attr[arg] != "-" else ""

                        case "w" | "west":  # w: width style color
                            style += f"border-left: {attr[arg]}; " if attr[arg] != "-" else ""

                        case "r" | "radi" | "radius":  # r: nw ne se sw
                            style += f"border-radius: {attr[arg]}; " if attr[arg] != "-" else ""
                return style, None

            case "curs" | "cursor":  # curs: curser-type response caret-color
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"cursor: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"pointer-events: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                    if len(attr_spl) > 2:
                        style += f"caret-color: {attr_spl[2]}; " if attr_spl[2] != "-" else ""
                return style, None

            case "font":  # font: font-style font-variant font-weight size font-family
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"font-style: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"font-variant: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                    if len(attr_spl) > 2:
                        style += f"font-weight: {attr_spl[2]}; " if attr_spl[2] != "-" else ""
                        if len(attr_spl) > 3:
                            style += f"font-size: {attr_spl[3]}; " if attr_spl[3] != "-" else ""
                            if len(attr_spl) > 4:
                                style += f"font-family: {attr_spl[4].replace('(', '').replace(')', '')}; " \
                                    if attr_spl[4] != "-" else ""
                return style, None

            case "list":  # list: marker-type marker-image marker-position
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"list-style-type: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"list-style-image: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                    if len(attr_spl) > 2:
                        style += f"list-style-position: {attr_spl[2]}; " if attr_spl[2] != "-" else ""
                return style, None

            case "marg" | "margin":  # marg: t r b l
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"margin-top: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"margin-right: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                    if len(attr_spl) > 2:
                        style += f"margin-bottom: {attr_spl[2]}; " if attr_spl[2] != "-" else ""
                        if len(attr_spl) > 3:
                            style += f"margin-left: {attr_spl[3]}; " if attr_spl[3] != "-" else ""
                return style, None

            case "maxs" | "maxsize":
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"max-width: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"max-height: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                return style, None

            case "mins" | "minsize":
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"min-width: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"min-height: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                return style, None

            case "outl" | "outline":
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"outline-width: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"outline-offset: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                    if len(attr_spl) > 2:
                        style += f"outline-style: {attr_spl[2]}; " if attr_spl[2] != "-" else ""
                        if len(attr_spl) > 3:
                            style += f"outline-color: {attr_spl[3]}; " if attr_spl[3] != "-" else ""
                return style, None

            case "over" | "overflow":
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"overflow-x: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"overflow-y: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                return style, None

            case "padd" | "padding":  # padg: t r b l
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"padding-top: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"padding-right: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                    if len(attr_spl) > 2:
                        style += f"padding-bottom: {attr_spl[2]}; " if attr_spl[2] != "-" else ""
                        if len(attr_spl) > 3:
                            style += f"padding-left: {attr_spl[3]}; " if attr_spl[3] != "-" else ""
                return style, None

            case "posi" | "position":
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"position: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    if len(attr_spl) > 2:
                        style += f"{'left' if attr_spl[1][1] == 'w' else 'right'}: " \
                                 f"{attr_spl[2]}; " if attr_spl[2] != "-" else ""
                        if len(attr_spl) > 3:
                            style += f"{'top' if attr_spl[1][0] == 'n' else 'bottom'}: " \
                                     f"{attr_spl[3]}; " if attr_spl[3] != "-" else ""
                            if len(attr_spl) > 4:
                                style += f"z-index: {attr_spl[4]}; " if attr_spl[4] != "-" else ""
                return style, None

            case "size":
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"width: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"height: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                return style, None

            case "tabl" | "table":  # tabl: layout caption-side empty-cells
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"table-layout: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"caption-side: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                    if len(attr_spl) > 2:
                        style += f"empty-cells: {attr_spl[2]}; " if attr_spl[2] != "-" else ""
                return style, None

            case "text":
                style = ""
                for arg in attr:
                    attr_spl = BaseEngine.__safe_split(attr[arg])
                    match arg:
                        case "a" | "alig" | "align":  # a: all last_line
                            style += f"text-align: {attr_spl[0]}; " if attr_spl[0] != "-" else ""

                            style += f"text-align-last: {attr_spl[1]}; " if attr_spl[1] != "-" else ""

                        case "l" | "line":  # l: type(underline/overline/line-through) style color
                            style += f"text-decoration: {attr_spl[0]} {attr_spl[2]} {attr_spl[1]}; "

                        case "f" | "form" | "format":  # f: indent overflow transform line-height letter-spacing dir
                            style += f"text-indent: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                            if len(attr_spl) > 1:
                                style += f"text-overflow: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                                if len(attr_spl) > 2:
                                    style += f"text-transform: {attr_spl[2]}; " if attr_spl[2] != "-" else ""
                                    if len(attr_spl) > 3:
                                        style += f"line-height: {attr_spl[3]}; " if attr_spl[3] != "-" else ""
                                        if len(attr_spl) > 4:
                                            style += f"letter-spacing: {attr_spl[4]}; " if attr_spl[4] != "-" else ""
                                            if len(attr_spl) > 5:
                                                style += f"direction: {attr_spl[5]}; " if attr_spl[5] != "-" else ""

                        case "c" | "colo" | "color":  # s: x y blur-radius color
                            style += f"color: {attr[arg]}; "

                        case "s" | "sele" | "select":  # r: nw ne se sw
                            style = f"user-select: {attr[arg]}; " if attr[arg] != "-" else ""
                return style, None

            case "tran" | "transform":
                style = ""
                for arg in attr:
                    attr_spl = BaseEngine.__safe_split(attr[arg])
                    match arg:
                        case "a" | "appl" | "apply":  # a: transforms (eg.: scale(2) rotate(25deg))
                            if isinstance(attr, dict):
                                style += f"transform: {attr[arg]}; "
                            else:
                                style += f"transform: {attr}; "

                        case "o" | "orig" | "origin":  # o: x y z
                            style += f"transform-origin: {attr_spl[0]} {attr_spl[1]} {attr_spl[2]}; "

                        case "c" | "chil" | "children":  # c: mode (preserve-3d/flat)
                            style += f"text-indent: {attr[arg]}; "
                return style, None

            case "visi" | "visibility":
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"visibility: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"opacity: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                    if len(attr_spl) > 2:
                        style += f"display: {attr_spl[2]}; " if attr_spl[2] != "-" else ""
                        if len(attr_spl) > 3:
                            style += f"backface-visibility: {attr_spl[3]}; " if attr_spl[3] != "-" else ""
                            if len(attr_spl) > 4:
                                style += f"filter: {attr_spl[4]}; " if attr_spl[4] != "-" else ""
                return style, None

            case "word":  # word: wrap spacing writing-mode hyphens
                attr_spl = BaseEngine.__safe_split(attr)
                style = f"word-break: {attr_spl[0]}; " if attr_spl[0] != "-" else ""
                if len(attr_spl) > 1:
                    style += f"word-spacing: {attr_spl[1]}; " if attr_spl[1] != "-" else ""
                    if len(attr_spl) > 2:
                        style += f"writing-mode: {attr_spl[2]}; " if attr_spl[2] != "-" else ""
                        if len(attr_spl) > 3:
                            style += f"hyphens: {attr_spl[3]}; " if attr_spl[3] != "-" else ""
                return style, None

            case "_css":
                return attr

            case _:
                raise ValueError(f"Unknown style argument '{key}'.")

    @staticmethod
    def __parse_animations(animations: dict):
        out = ""
        if animations:
            for name, keyframes in list(animations.items()):
                out += "@keyframes " + name + " {"
                for keyframe, style in list(keyframes.items()):
                    out += keyframe + " {" + BaseEngine.__parse_css(style)[0] + "} "
                out += "}\n"
            return out if out else ""
        else:
            return ""

    @staticmethod
    def __parse_css(css: dict):
        style = ""
        classes = ""
        for arg in css:
            try:
                s = BaseEngine.__css_from_attr(arg, css[arg])
            except ValueError:
                raise
            except:
                raise StyleParseError(f"Error while parsing style argument '{arg}' with value '{css[arg]}'")
            style += s[0]
            if s[1]:
                classes += s[1] + " "
        return style.rstrip(), classes.rstrip()

    @staticmethod
    def __load_objects(objects):
        out = {}
        _temp = '"'
        pattern = '<{_type} class="{classes}" id="{_id if _id else None}" ' \
                  '{("style=" + _temp + css + _temp) if css else ""}' \
                  '{" " if args else ""}{" ".join(args)}>{_text}​</{_type}>'
        for obj in objects:
            args = [
                f'{BaseEngine.__html_kw.get(kw, "")}="{objects[obj].get(kw, "")}"'
                for kw in objects[obj] if BaseEngine.__html_kw.get(kw, "")
            ]
            _id = obj
            if not objects[obj].get("type", None):
                raise AttributeError(f"Parameter 'type' for object '{_id}' has not been specified.")

            _type = BaseEngine.__type_kw.get(objects[obj].get("type", None), None)

            if not _type:
                raise ValueError(f"Unknown type '{objects[obj].get('type', None)}' in object '{_id}'.")

            _text = objects[obj].get("text", "").replace(r"\n", "<br>")

            css, classes = BaseEngine.__parse_css(objects[obj].get("styl", ""))

            out[obj] = eval(f"f'{pattern}'")

        return out

    @staticmethod
    def __arrange_objects(obj_htmls, structure):
        def recursive_loop(struct):
            if isinstance(struct, list):
                return "".join(recursive_loop(element) for element in struct)

            if isinstance(struct, dict):
                element_html = obj_htmls.get(list(struct.items())[0][0])
                return element_html.replace("​", recursive_loop(list(struct.items())[0][1]))

            else:
                element_html = obj_htmls.get(struct, "")
                if not element_html:
                    raise StructureError(f"Unknown object '{struct}'.")
                else:
                    return element_html

        if structure and obj_htmls:
            return recursive_loop(structure).replace("​", "")
        else:
            return ""
