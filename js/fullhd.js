var rule = {
    title:'fullhd',
    host:'https://www.fullhd.to',
    //homeUrl:'/zh',
    url:'/fyclass/fypage/[/fyclass/]',
    searchUrl:'/search/**/',
    searchable:2,
    headers:'User-Agent$MOBILE_UA#Referer$https://www.fullhd.to#Accept$text/html,image/jpeg,*/*#Accept-Language$zh-CN,zh;q=0.8',
    timeout:5000,
    class_url:'latest-updates&top-rated&most-popular&networks/brazzers-com&networks/tushy-com&networks/naughtyamerica-com&sites/sexmex&sites/passion-hd&categories/animation&categories/18-years-old&categories/pawg&categories/thong&categories/stockings&categories/jav-uncensored&categories/pantyhose',
    class_name:'最新&最佳&热门&Brazzers&Tushy&NaughtyA&Sexmex&Passion&动画&18岁&丰臀女孩&丁字裤&丝袜&日本未审查&连裤袜',
    //class_name:'#page-viewport&&ul&&li;.text&&Text;a&&href;/(.*)',
    cate_exclude:'应用',
    //推荐:'a.thumb_img;pd(this,"&&title","测试标题");img&&src;span.duration&&Text;a&&href',
    double:false,
    limit:50,
    play_parse:false,
    一级:'a.thumb_img;&&title;img&&data-src;span.duration&&Text;href',
    推荐:"*",
    //二级:';;;;;video;source&&label;source&&src',
    二级:{
        title: "1",          // 片名选择器
        img: "video&&poster",       // 详情页封面
        desc: "类型",
        content:"简介",     // 简介
        tabs:"video",       // 线路/标签外层容器
        lists:"source",   // 每一条线路对应的选集容器，#id会自动替换线路下标
        tab_text:"线路",      // 线路名称文本提取
        list_text:"source&&label",       // 单集的集数名称
        list_url:"source&&src",         // 单集播放链接
        "重定向":""
    },

    搜索:'a.thumb_img;&&title;img&&src;span.duration&&Text;&&href',
}
