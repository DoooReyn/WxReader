// --------------------------- 基础支持 ---------------------------

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

// --------------------------- 切换主题 ---------------------------

/**
 * 点击切换主题
 */
function changeTheme() {
    const white = document.querySelector('.readerControls_item.white')
    const dark = document.querySelector('.readerControls_item.dark')
    white && pressMouseKey(white);
    dark && pressMouseKey(dark);
}

// --------------------------- 导出笔记 ---------------------------

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
    savedNotes(`${book}.md`, notes.join('\n'));
}

// --------------------------- 缓存数据 ---------------------------

const Action = {
    ScrollToEnd: 1,
    ReadingFinished: 2
}

const Cache = {
    HasSelection: false
}

// --------------------------- 选中状态 ---------------------------

/**
 * 监听选中状态
 */
function watchSelection() {
    const MutationObserver = window['MutationObserver'] || window['WebKitMutationObserver'] || window['MozMutationObserver']

    const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.type === 'attributes') {
                Cache.HasSelection = mutation.target.style.display ? false : true;
                updateState(`选中状态改变 ${Cache.HasSelection}`);
            }
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
            Cache.HasSelection = selection && selection.toString() !== '';
        })
        const element_toolbar = document.querySelector('.reader_toolbar_container');
        listen(element_toolbar);
    }

    // reader_toolbar_container 在加载后并未创建，因此先要监听他的父节点
    const element_container = document.querySelector('.renderTargetContainer');
    const observer_container = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            for (const node of mutation.addedNodes) {
                if (node.className === 'reader_toolbar_container') {
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
}

// --------------------------- 自动滚动 ---------------------------

/**
 * 是否已滚动到底部
 */
function isScrollToEnd() {
    // 变量scrollTop是滚动条滚动时，滚动条上端距离顶部的距离
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    // 变量windowHeight是可视区的高度
    const windowHeight = document.documentElement.clientHeight || document.body.clientHeight;
    // 变量scrollHeight是滚动条的总高度（当前可滚动的页面的总高度）
    const scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
    // 滚动条到底部
    return scrollTop + windowHeight >= scrollHeight;
}

/**
 * 滚动监听
 */
function watchScroll() {
    document.onscroll = function () {
        if (isScrollToEnd()) {
            sendAction(Action.ScrollToEnd);
        }
    };
}

/**
 * 切换下一章
 */
function nextChapter() {
    if (isPageLoading()) return;

    let element = document.querySelector('.readerFooter_button');
    if (element) {
        // 下一章: 按下向右按键（按键码39）
        updateState('正在切换下一章')
        fireKeyEvent(39);
    } else {
        // 找不到下一章时，查看全文是否已结束
        let done = document.querySelector('.readerFooter_ending');
        if (done) {
            updateState('全书完.');
            sendAction(Action.ReadingFinished);
            alert('全书完.')
        }
    }
    Cache.HasSelection = false;
}

/**
 * 页面是否正在加载中
 * @return {boolean}
 */
function isPageLoading() {
    return document.querySelector('.readerChapterContentLoading') ? true : false;
}

/**
 * 执行滚动
 * 调用此方法的间隔必须大于 16.7 ms
 */
function doScroll(offset_y = 0) {
    if (isPageLoading()) {
        updateState("页面加载中...");
        return;
    }

    if (Cache.HasSelection) {
        updateState("暂停");
        return;
    }

    if (isScrollToEnd()) {
        sendAction(Action.ScrollToEnd);
        return;
    }

    const top = (document.documentElement.scrollTop || document.body.scrollTop) + offset_y;
    scroll({left: 0, top: top, behavior: 'smooth'});
    updateState(`自动阅读中...`);
}

window.onload = function () {
    watchScroll();
    watchSelection();
}
