$(document).ready(function() {

  //Initialize Smooth Scroll
  smoothScroll.init({
      updateURL: false,
  });
  
  //Open external links in new tab
  $(function() { 
    $('a[rel*=external]').click( function() {
      window.open(this.href);
      return false;
    });
  });
  
});
