/*
Copyright 2022 DoooReyn

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

/**
 * 数据缓存区
 * @type {{HasSelection: number}}
 */
const SwapData = {
    HasSelection: 0
}

/**
 * 阅读器动作
 * @type {{ExportNote: number, HasSelection: number, NextTheme: number}}
 */
const ReaderActions = {
    WatchSelection: 11,
    ExportNote: 5,
    NextTheme: 6,
}


/**
 * 监听选中状态
 */
function watchSelection() {
    const MutationObserver = window['MutationObserver'] || window['WebKitMutationObserver'] || window['MozMutationObserver']

    /**
     * 设置选中状态
     */
    function setSelection() {
        pjTransport && pjTransport.setSelection(SwapData.HasSelection);
    }

    /**
     * 选中监听
     */
    function watch() {
        document.addEventListener('selectionchange', function () {
            let selection = window.getSelection()
            if (selection && selection.toString() !== '') {
                SwapData.HasSelection = 1;
            } else {
                SwapData.HasSelection = 0;
            }
            setSelection();
        })

        const element_toolbar = document.querySelector('.reader_toolbar_container');
        const observer_toolbar = new MutationObserver(function (mutations) {
            mutations.forEach(function (mutation) {
                if (mutation.type === 'attributes') {
                    SwapData.HasSelection = mutation.target.style.display ? 0 : 1;
                    pjTransport && pjTransport.j2p('选中状态改变');
                    setSelection();
                }
            });
        });
        observer_toolbar.observe(element_toolbar, {
            attributes: true,
            attributeFilter: ['style']
        });
        pjTransport && pjTransport.j2p('选中监听已启动！');
    }

    // reader_toolbar_container 在加载后并未创建，因此先要监听他的父节点
    const element_container = document.querySelector('.renderTargetContainer');
    const observer_container = new MutationObserver(function (mutations, observe) {
        mutations.forEach(function (mutation) {
            for (const node of mutation.addedNodes) {
                if (node.className === 'reader_toolbar_container') {
                    pjTransport && pjTransport.j2p('选中监听启动中...');
                    watch();
                    break;
                }
            }
        })
    });
    observer_container.observe(element_container, {
        childList: true,
    });
    pjTransport && pjTransport.j2p('正在启用选中监听');
}


/**
 * 在元素上模拟鼠标按下事件
 * @param {string} elementName
 */
function pressMouseKey(elementName) {
    let elements = document.getElementsByClassName(elementName);
    if (elements && elements.length > 0) {
        let clickEvent = document.createEvent('MouseEvent');
        clickEvent.initMouseEvent(
            'click',
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
    let notes_elements = document.getElementsByClassName('sectionListItem');
    if (notes_elements.length === 0) {
        return alert('你还没有做笔记哦！');
    }
}

/**
 * 点击切换主题
 */
function changeTheme() {
    !pressMouseKey('readerControls_item white') &&
    pressMouseKey('readerControls_item dark');
}

window.onload = function () {
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.pjTransport = channel.objects.pjTransport;
        pjTransport.p2j.connect(function (code) {
            console.log('[js2py]', code);
            pjTransport.j2p(code);
            if (code === ReaderActions.ExportNote) {
                exportNotes();
            } else if (code === ReaderActions.NextTheme) {
                changeTheme();
            } else if (code === ReaderActions.WatchSelection) {
                watchSelection()
            }
        })

        // 自动启用选中监听
        watchSelection();
    });
}
