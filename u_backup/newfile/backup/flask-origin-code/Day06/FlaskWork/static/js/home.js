$(function () {
    var swiper = new Swiper('.swiper-container', {
        pagination: '.swiper-pagination',
        paginationClickable: true,
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
        spaceBetween: 30,
        effect: 'fade'
    });


    $(".movie-like").click(function () {

        var $movie_like = $(this);

        var movie_id = $movie_like.attr("movie_id");

        $.post("/movies/collect/",{"movie_id": movie_id}, function (data) {
            console.log(data);

            if(data["status"] === 900){
                window.open("/users/login/", target="_self");
            }else if(data["status"] === 902){
                $movie_like.children().css("color", "red");
            }

        }, "json")

    });
    $(".onclick").click(function () {
        $(".movie_list_collect").css.display = "block";
        $(".movie_list_recommend").css.display = "none";

        // var $movie_liked = $(this);
        //
        // var movie_id = $movie_liked.attr("movie_id");
        //
        // $.post("/movies/collect/",{"movie_id": movie_id}, function (data) {
        //     console.log(data);
        //
        //     if(data["status"] === 900){
        //         window.open("/users/login/", target="_self");
        //     }else if(data["status"] === 902){
        //         $movie_like.children().css("color", "red");
        //     }
        //
        // }, "json")

    });

});
