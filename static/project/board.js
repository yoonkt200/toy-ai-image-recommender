/**
 * Created by daddyslab on 2017. 1. 21..
 */

$(document).ready(function () {
    var searchText = $('.hidden_searchText').text();

    var currentPage = $('.hidden_currentPage').text();
    var pages = $('.page_all').length;
    var page_area = Math.ceil((pages/5));
    var current_area = Math.ceil((currentPage/5));

    // 페이지 네이게이션 초기 배치 if-else
    if(page_area == 1){ // 페이지 구역이 1개
        $('.first').hide();
        $('.prev').hide();
        $('.next').hide();
        $('.last').hide();
    } else if(page_area == 2){ // 페이지 구역이 2개
        if(current_area == page_area){
            $('.first').hide();
            $('.next').hide();
            $('.last').hide();
        } else{
            $('.first').hide();
            $('.prev').hide();
            $('.last').hide();
        }
    } else if(page_area == 3){ // 페이지 구역이 3개
        if(current_area == page_area){
            $('.next').hide();
            $('.last').hide();
        } else if(current_area == 1){
            $('.first').hide();
            $('.prev').hide();
        } else{
            $('.first').hide();
            $('.last').hide();
        }
    } else if(page_area == 4){ // 페이지 구역이 4개
        if(current_area == page_area){
            $('.next').hide();
            $('.last').hide();
        } else if(current_area == 3){
            $('.last').hide();
        } else if(current_area == 2){
            $('.first').hide();
        } else{
            $('.first').hide();
            $('.prev').hide();
        }
    } else{ // 페이지 구역이 5개 이상
        if(current_area == page_area){
            $('.next').hide();
            $('.last').hide();
        } else if(current_area == (page_area - 1)){
            $('.last').hide();
        } else if(current_area == 2){
            $('.first').hide();
        } else if(current_area == 1){
            $('.first').hide();
            $('.prev').hide();
        } else{
            // all show()
        }
    }

    // current area 링크를 제외하고 hide()
    var area_min = ((current_area * 5) - 4) - 1;
    var area_max = (current_area * 5) - 1;
    $('.page_all').each(function (index, element) {
        if(! ((area_min <= index) && (index <= area_max)) ){
            $(element).hide();
        }
    });

    // 검색 text 여부에 따라 url 파라미터 설정 : 페이지 네비게이션 화살표 링크
    var parameter = ''
    if(searchText == 'none'){
        parameter = '?';
    } else{
        parameter = '?search=' + searchText + "&";
    }
    $('.first').click(function () {
        window.location.href = "/board" + parameter + "page=" + 1;
    });
    $('.prev').click(function () {
        window.location.href = "/board" + parameter + "page=" + (((current_area - 1) * 5) - 4);
    });
    $('.next').click(function () {
        window.location.href = "/board" + parameter + "page=" + (((current_area + 1) * 5) - 4);
    });
    $('.last').click(function () {
        window.location.href = "/board" + parameter + "page=" + pages;
    });

    // 검색 버튼
    $('.project_search_btn').click(function () {
        var searchText = $('.project_search_input').val();
        window.location.href = "/board?search=" + searchText;
    });

    $('.page_all').click(function () {
        var number = $(this).find("li").text();
        var nav = "/board" + parameter + "page=" + number;
        $(this).attr("href", nav);
        window.location.href = "/board" + parameter + "page=" + pages;
    });
}) 