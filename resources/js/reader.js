/*
Copyright 2022 DoooReyn

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

const ReaderActions = {
    BackHome: 0,
    Refresh: 1,
    Scrollable: 2,
    SpeedDown: 3,
    SpeedUp: 4,
    ExportNote: 5,
    NextTheme: 6,
}


/**
 * 在元素上模拟鼠标按下事件
 * @param {string} elementName
 */
function pressMouseKey(elementName) {
    let elements = document.getElementsByClassName(elementName);
    if (elements && elements.length > 0) {
        let clickEvent = document.createEvent("MouseEvent");
        clickEvent.initMouseEvent(
            "click",
            false,
            false,
            window,
            0,
            0,
            0,
            0,
            0,
            false,
            false,
            false,
            false,
            0,
            null
        );
        elements[0].dispatchEvent(clickEvent);
        return true;
    }
    return false;
}

/**
 * 导出笔记
 */
function exportNotes() {
    let notes_elements = document.getElementsByClassName("sectionListItem");
    if (notes_elements.length === 0) {
        return alert('你还没有做笔记哦！');
    }
}

/**
 * 点击切换主题
 */
function changeTheme() {
    !pressMouseKey("readerControls_item white") &&
    pressMouseKey("readerControls_item dark");
}

window.onload = function () {
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.pjTransport = channel.objects.pjTransport;
        pjTransport.p2j.connect(function (code) {
            console.log("[js2py]", code);
            pjTransport.j2p(code.toString());

            if (code === ReaderActions.ExportNote) {
                exportNotes();
            } else if (code === ReaderActions.NextTheme) {
                changeTheme();
            }
        })
    });
}
