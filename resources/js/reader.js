/*
Copyright 2022 DoooReyn

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

/**
 * 数据缓存区
 * @type {{HasSelection: number, ScrollToEnd: number, Loading: number, Speed: number, Scrollable: boolean}}
 */
const SwapData = {
    HasSelection: 0,
    ScrollToEnd: 0,
    Loading: 0,
    Speed: 1,
    Scrollable: false
}

/**
 * 阅读器动作
 * @type {{ExportNote: number, WatchSelection: number, NextTheme: number}}
 */
const ReaderActions = {
    Scrollable: 2,
    ExportNote: 5,
    NextTheme: 6,
    WatchSelection: 11,
    Scrolling: 12,
    CheckLoading: 13,
    ScrollableOff: 20,
    ScrollableOn: 21,
}

/**
 * 发送消息给 Python
 * @param tip 消息
 */
function sendToPy(tip) {
    pjTransport && pjTransport.j2p(tip);
}

/**
 * 设置选中状态
 * @param {number} value
 */
function setSelection(value) {
    SwapData.HasSelection = value;
    pjTransport && pjTransport.setSelection(SwapData.HasSelection);
}

/**
 * 设置是否已滚动到底部
 * @param {number} value
 */
function setScrollToEnd(value) {
    SwapData.ScrollToEnd = value;
    pjTransport && pjTransport.setScrollToEnd(SwapData.ScrollToEnd);
}

/**
 * 检查滚动状态
 */
function checkScrolling() {
    // 变量scrollTop是滚动条滚动时，滚动条上端距离顶部的距离
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    // 变量windowHeight是可视区的高度
    const windowHeight = document.documentElement.clientHeight || document.body.clientHeight;
    // 变量scrollHeight是滚动条的总高度（当前可滚动的页面的总高度）
    const scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
    // 滚动条到底部
    if (scrollTop + windowHeight >= scrollHeight) {
        // 要进行的操作
        setScrollToEnd(1);
        onScrollToEnd();
    } else {
        setScrollToEnd(0);
    }
}

/**
 * 滚动监听
 */
function watchScroll() {
    document.onscroll = checkScrolling;
    sendToPy('滚动监听已启动！');
}

/**
 * 执行滚动
 */
function doScroll() {
    checkScrolling();
    if (!SwapData.ScrollToEnd) {
        const top = document.documentElement.scrollTop || document.body.scrollTop;
        window.scroll({left: 0, top: top + SwapData.Speed, behavior: 'smooth'});
    }
}

/**
 * 滚动到底部回调
 */
function onScrollToEnd() {
    if (!SwapData.Scrollable) return sendToPy("未开启自动阅读");
    if (SwapData.ScrollToEnd === 0) return sendToPy("未滚动到底部");

    let element = document.querySelector('.readerFooter_button');
    if (element) {
        // 下一章: 按下向右按键（按键码39）
        sendToPy('正在切换下一章')
        fireKeyEvent(39);
        setSelection(0);
        setScrollToEnd(0);
    } else {
        // 找不到下一章时，查看全文是否已结束
        let done = document.querySelector('.readerFooter_ending');
        if (done) {
            pjTransport && pjTransport.readingFinished();
            sendToPy('全书已读完.');
            // alert('全书已读完.')
        } else {
            sendToPy('糟糕，未检测到的情况！')
        }
    }
}

/**
 * 监听选中状态
 */
function watchSelection() {
    const MutationObserver = window['MutationObserver'] || window['WebKitMutationObserver'] || window['MozMutationObserver']

    const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.type === 'attributes') {
                setSelection(mutation.target.style.display ? 0 : 1);
                sendToPy('选中状态改变');
            }
            console.log(mutation)
        });
    });

    const listen = (e) => {
        e && observer.observe(e, {
            attributes: true,
            // attributeFilter: ['style'],
            childList: true
        });
    }

    /**
     * 选中监听
     */
    function watch() {
        document.addEventListener('selectionchange', function () {
            let selection = window.getSelection()
            if (selection && selection.toString() !== '') {
                setSelection(1);
            } else {
                setSelection(0);
            }
        })

        const element_toolbar = document.querySelector('.reader_toolbar_container');
        listen(element_toolbar);

        sendToPy('选中监听已启动！');
    }

    // reader_toolbar_container 在加载后并未创建，因此先要监听他的父节点
    const element_container = document.querySelector('.renderTargetContainer');
    const observer_container = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            for (const node of mutation.addedNodes) {
                if (node.className === 'reader_toolbar_container') {
                    sendToPy('选中监听启动中...');
                    watch();
                    break;
                }
            }
        })
    });
    observer_container.observe(element_container, {
        childList: true,
    });

    const element_catalog = document.querySelector('.readerCatalog');
    const element_note = document.querySelector('.readerNotePanel');
    listen(element_catalog);
    listen(element_note);

    sendToPy('正在启用选中监听');
}

/**
 * 页面是否正在加载中
 * @return {boolean}
 */
function setPageLoading() {
    SwapData.Loading = document.querySelector('.readerChapterContentLoading') ? 1 : 0;
    pjTransport && pjTransport.setPageLoading(SwapData.Loading);
}

/**
 * 在元素上模拟鼠标按下事件
 * @param {string|HTMLElement} selector
 */
function pressMouseKey(selector) {
    let element = (selector instanceof HTMLElement) ? selector : document.querySelector(selector);
    if (element) {
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
        element.dispatchEvent(clickEvent);
        return true;
    }
    return false;
}


/**
 * 模拟发送键盘事件
 * @param {number} key_code
 */
function fireKeyEvent(key_code) {
    const ke = new KeyboardEvent('keydown', {
        bubbles: true, cancelable: true, keyCode: key_code
    });
    document.body.dispatchEvent(ke);
}


/**
 * 获取格式化后的内容
 * @param {string} prefix
 * @param {string} para
 */
function formatContent(prefix, para) {
    let result = [];
    let contents = para.split('\n');
    for (let i = 0; i < contents.length; i++) {
        contents[i].replace(/\s*/g, '').length > 0 &&
        result.push(prefix + contents[i]);
    }
    return result.join('\n' + prefix + '\n');
}

/**
 * 获取格式化后的想法
 * @param {string} para
 * @param {string} thought
 */
function formatNoteThought(para, thought) {
    let t = formatContent('  > ', para);
    let l = '    >> 想法：\n    >>';
    let p = formatContent('    >> ', thought);
    return [t, l, p].join('\n') + '\n';
}

/**
 * 获取格式化后的段落
 * @param {string} para
 */
function formatNoteParagraph(para) {
    return formatContent('  > ', para) + '\n';
}

/**
 * 获取格式化后的章节标题
 * @param {string} title
 */
function formatNoteTitle(title) {
    return '## ' + title + '\n';
}

/**
 * 获取格式化后的书名标题
 * @param {string} header
 */
function formatNoteHeader(header) {
    return '# 《' + header + '》读书笔记\n';
}

/**
 * 导出笔记
 */
function exportNotes() {
    let notes_elements = document.querySelectorAll('.sectionListItem');
    if (notes_elements.length === 0) {
        return alert('你还没有做笔记哦！');
    }

    let book = document.querySelector('.readerCatalog_bookInfo_title_txt').innerText;
    let notes = [formatNoteHeader(book)];
    for (let i = 0; i < notes_elements.length; i++) {
        let ele = notes_elements[i];
        let titles = ele.getElementsByClassName('sectionListItem_title');
        let abstracts = ele.getElementsByClassName('abstract');
        let texts = ele.getElementsByClassName('text');
        titles.length > 0 && notes.push(formatNoteTitle(titles[0].innerText));
        if (abstracts.length > 0) {
            const note = formatNoteThought(abstracts[0].innerText, texts[0].innerText)
            notes.push(note);
        } else {
            notes.push(formatNoteParagraph(texts[0].innerText));
        }
    }
    pjTransport && pjTransport.downloadNote(`${book}.md`, notes.join('\n'));
}

/**
 * 点击切换主题
 */
function changeTheme() {
    const white = document.querySelector('.readerControls_item.white')
    const dark = document.querySelector('.readerControls_item.dark')
    white && pressMouseKey(white);
    dark && pressMouseKey(dark);
}

/**
 * 载入 QWebContent
 */
window.onload = function () {
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.pjTransport = channel.objects.pjTransport;

        pjTransport.p2j.connect(function (code) {
            // sendToPy(`正在应用阅读器动作: ${code}`);
            if (code === ReaderActions.ExportNote) {
                sendToPy('正在尝试导出笔记');
                exportNotes();
            } else if (code === ReaderActions.NextTheme) {
                changeTheme();
            } else if (code === ReaderActions.WatchSelection) {
                watchSelection();
                watchScroll();
            } else if (code === ReaderActions.Scrolling) {
                doScroll();
            } else if (code === ReaderActions.CheckLoading) {
                setPageLoading();
            } else if (code === ReaderActions.ScrollableOff) {
                SwapData.Scrollable = false;
                sendToPy("已关闭自动阅读");
            } else if (code === ReaderActions.ScrollableOn) {
                SwapData.Scrollable = true;
                sendToPy("已开启自动阅读");
            } else if (code > 1000) {
                // 使用新的信号竟然不生效，暂时使用这种 Hack 方式来实现速度调节
                const speed = code - 1000;
                SwapData.Speed = speed;
                localStorage.setItem('speed', speed.toString());
                sendToPy(`正在应用页面滚动速度: ${speed}`);
            }
        })

        SwapData.Speed = parseInt(localStorage.getItem('speed') || '1');

        // 自动启用选中监听
        watchSelection();

        // 自动开启滚动监听
        watchScroll();
    });
}
