$(function() {

  // :)
  var placeholders = [
    {
      comic: "Detective Comics",
      email: "bruce@wayneenterprises.com"
    },
    {
      comic: "Iron Man",
      email: "tony@starkindustries.com"
    },
    {
      comic: "Superior Spider-Man",
      email: "droctavius@empirestate.edu"
    },
    {
      comic: "Avengers",
      email: "director@shield.gov",
    },
    {
      comic: "Action Comics",
      email: "ckent@dailyplanet.com"
    }
  ];

  var i = 0;

  var cyclePlaceholders = function() {
    i++;
    if (i == placeholders.length) i = 0;
    $("#search").attr('placeholder', placeholders[i].comic);
    $("#email").attr('placeholder', placeholders[i].email);
  }

  setInterval(cyclePlaceholders, 3000);
});
