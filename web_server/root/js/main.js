"use strict";
var visible = true;

function toggleImageVis()
{
    var element = document.getElementById("wolf_logo");
    if (visible)
    {
        element.style.visibility = "hidden";
        visible = false;
    }
    else
    {
        element.style.visibility = "visible";
        visible = true;
    }
}