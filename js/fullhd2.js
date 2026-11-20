var rule = {
    title:'fullhd',
    host:'https://www.fullhd.to',
    homeUrl:'/zh',
    url:'/fyclass/fypage/[/fyclass/]',
    searchUrl:'/search/**/',
    searchable:2,
    headers:'User-Agent$MOBILE_UA#Referer$https://www.fullhd.to#Accept$text/html/jpg#accept-language$zh-CN,zh;q=0.8',
    timeout:5000,
    class_url:'latest-updates&top-rated&most-popular&networks/brazzers-com&networks/tushy-com&networks/naughtyamerica-com&sites/sexmex&sites/passion-hd&categories/animation&categories/18-years-old&categories/pawg&categories/thong&categories/stockings&categories/jav-uncensored&categories/pantyhose',
    class_name:'最新&最佳&热门&Brazzers&Tushy&NaughtyA&Sexmex&Passion&动画&18岁&丰臀女孩&丁字裤&丝袜&日本未审查&连裤袜',
    //class_name:'#page-viewport&&ul&&li;.text&&Text;a&&href;/(.*)',
    cate_exclude:'应用',
    //推荐:'a.thumb_img;pd(this,"&&title","测试标题");img&&src;span.duration&&Text;a&&href',
一级:`js:
let htmlText = getHtml(MY_URL);
let arr = [];
let searchPos = 0;
while(true){
    let posThumb = htmlText.indexOf('class="thumb_img"', searchPos);
    if(posThumb === -1){
        break;
    }
    let posAStart = htmlText.lastIndexOf('<a ', posThumb);
    let posAEnd = htmlText.indexOf('</a>', posThumb);

    if(posThumb !== -1 && posAStart !== -1 && posAEnd !== -1){
        let aBlock = htmlText.substring(posAStart, posAEnd + 4);
        // href
        let mHref = aBlock.match(/href\s*=\s*["']([^"']+)["']/);
        let href = "";
        if(mHref){
            href = mHref[1];
        }
        // title
        let mTitle = aBlock.match(/title\s*=\s*["']([^"']+)["']/);
        let title = "无标题";
        if(mTitle){
            title = mTitle[1];
        }
        // ========== 从href路径 /videos/后面截取数字ID，切掉末尾3位 ==========
        let objId = "";
        let imgSrc = "";
        if(href){
            let key = "/videos/";
            let sPos = href.indexOf(key);
            if(sPos !== -1){
                let idStart = sPos + key.length;
                let ePos = href.indexOf("/", idStart);
                if(ePos !== -1){
                    objId = href.substring(idStart, ePos);
                    //if(objId.length >= 3){
                    //    objId = objId.substring(0, objId.length - 3);
                    //}
                }
            }
            // ⚠️务必替换为站点真实图片URL模板
            if(objId){
                imgSrc = "https://img.fullhd.to/"+objId.substring(0, objId.length - 3)+"000/"+objId+"/small/1.jpg";
    // 请求图片，带上referer
    //let imgBin = getBinary(imgSrc);//, {
    //    headers:{
   //         "Referer":"https://www.fullhd.to"
    //    }
    //})
    // 二进制转 base64
    //let b64 = toBase64(imgBin);
    //vod_pic = "data:image/jpeg;base64," + b64;
            }
        }
        // duration（副标题）
        let mDur = aBlock.match(/<span class="duration">(.*)span>/);
        let dur = "";
        if(mDur){
            dur = mDur[1];
                    if(dur.length > 3){
                        dur = dur.substring(0, dur.length - 2);
                    }
            //dur = mDur[1].substring(1, mDur[1].length - 2);
        }
        arr.push({
            vod_name: title,
            vod_pic: imgSrc,
            vod_remarks: dur,
            vod_id:href
        });
    }
    // 更新下一轮搜索起点，向后移动，防止死循环
    searchPos = posAEnd + 4;
}
VODS = arr;
`,
    double:false,
    limit:50,
    play_parse:false,
    //一级:'a.thumb_img;pd(this,"&&title","测试标题");img&&src;span.duration&&Text;href',
    推荐:"*",
    //二级:';;;;;video;source&&label;source&&src',
    //二级:{
     //   title: "1",          // 片名选择器
     //   img: "video&&poster",       // 详情页封面
     //   desc: "类型",
     //   content:"简介",     // 简介
     //   tabs:"video",       // 线路/标签外层容器
     //   lists:"source",   // 每一条线路对应的选集容器，#id会自动替换线路下标
     //   tab_text:"线路",      // 线路名称文本提取
     //   list_text:"source&&label",       // 单集的集数名称
     //   list_url:"source&&src",         // 单集播放链接
     //   重定向:""             // 拿到详情html之后执行js，可以返回新html
    //},
二级:`js:
    let detailHtml = getHtml(MY_URL);
    let baseHost = "https://www.fullhd.to"; //改成你的站点host

    // 1.截取video整块html
    let videoStart = detailHtml.indexOf("<video");
    let videoEnd = detailHtml.indexOf("</video>", videoStart);
    let videoHtml = "";
    if(videoStart !== -1 && videoEnd !== -1){
        videoHtml = detailHtml.substring(videoStart, videoEnd + "</video>".length);
    }

    // 2.提取video poster（详情封面图）
    let poster = "";
    let posterPos = videoHtml.indexOf('poster="');
    if(posterPos !== -1){
        let pStart = posterPos + 'poster="'.length;
        let pEnd = videoHtml.indexOf('"', pStart);
        if(pEnd !== -1){
            poster = videoHtml.substring(pStart, pEnd);
            if(poster && !poster.startsWith("http")){
                poster = baseHost + poster;
            }
        }
    }

    // 3.while循环抓取全部source标签（和你一级抓取条目写法一模一样！）
    let sourceList = [];
    let searchIdx = 0;
    while(true){
        let sStart = videoHtml.indexOf("<source", searchIdx);
        if(sStart === -1) break;
        let sEnd = videoHtml.indexOf(">", sStart);
        if(sEnd === -1) break;
        let sourceTag = videoHtml.substring(sStart, sEnd+1);

        // 提取 label
        let label = "";
        let labPos = sourceTag.indexOf('label="');
        if(labPos !== -1){
            let lS = labPos + 'label="'.length;
            let lE = sourceTag.indexOf('"', lS);
            if(lE !== -1) label = sourceTag.substring(lS,lE);
        }
        // 提取 src
        let src = "";
        let srcPos = sourceTag.indexOf('src="');
        if(srcPos !== -1){
            let sS = srcPos + 'src="'.length;
            let sE = sourceTag.indexOf('"', sS);
            if(sE !== -1) src = sourceTag.substring(sS,sE);
            if(src && !src.startsWith("http")){
                src = baseHost + src;
            }
        }
        if(label && src){
            sourceList.push({
                label: label,
                src: src
            })
        }
        searchIdx = sEnd + 1;
    }

    // 4.清晰度权重排序：480p优先→720p→1080p
    const qWeight = {
        "480p":1,
        "720p":2,
        "1080p":3
    };
    sourceList.forEach(item=>{
        let key = Object.keys(qWeight).find(k=> item.label.toLowerCase().includes(k));
        item.weight = key ? qWeight[key] : 999;
    })
    sourceList.sort((a,b)=> a.weight - b.weight);

    // 拼装引擎需要的选集字符串： label$src#label$src
    let urlsStr = sourceList.map(x=> `${x.label}$${x.src}`).join("#");

    // 返回整套二级vod详情对象
    let vodDetail = {
        title:"待替换标题", //后续在这里增加代码从detailHtml截取真实片名
        img: poster,
        desc:"待替换类型",  //类型
        content:"待替换简介",//简介
        vod_play_data:[
            {
                name:"线路",
                urls:urlsStr
            }
        ]
    };
    return vodDetail;
`,
    搜索:'a.thumb_img;&&title;img&&src;span.duration&&Text;&&href',
}
