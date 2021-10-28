// $(document).ready(function () {
//   $('#zoom_image').ezPlus({
//        zoomType: 'inner',
//		cursor: 'crosshair',
//		scrollZoom: true
//    });
//     $("#zoom_image").ezPlus({
//      gallery: 'zoom_image_gallery',
//      cursor: 'pointer',
//      galleryActiveClass: "active",
//      imageCrossfade: true,
//      loadingIcon: "images/spinner.gif"
//    });
//    $("#zoom_image").bind("click", function (e) {
//      var ez = $('#zoom_03').data('ezPlus');
//      ez.closeAll();
//      $.fancybox(ez.getGalleryList());
//      return false;
//    });
// });

//$(document).ready(function(){
//var quantity=0;
//   $('.quantity-right-plus').click(function(e){
//        e.preventDefault();
//        quantity = parseFloat($('#quantity').val());
//        $('#quantity').val(quantity + 0.5);
//    });
//     $('.quantity-left-minus').click(function(e){
//        e.preventDefault();
//        quantity = parseFloat($('#quantity').val());
//        if(quantity>0.5)
//        { $('#quantity').val(quantity - 0.5); }
//    });
//});