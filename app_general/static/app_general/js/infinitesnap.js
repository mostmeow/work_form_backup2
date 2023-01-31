// Hi! Warning: this JS was written in a single pre-coffee pass from top to bottom with zero concern for reusability or elegance. Purely a little experiment to see if it'd work.

var div = document.querySelector("#insnapdiv");
var nav = document.querySelector("#insnapnav");

// sorting images
function updateSort(el) {
    var scrollWidth = el.scrollWidth;
    var scrollLeft = el.scrollLeft;
    var width = el.offsetWidth;
    var items = el.children;

    if (scrollLeft <= width) {
        el.prepend(items[items.length - 1]);
        el.scrollLeft = scrollLeft + width;
    }
    if (scrollWidth - scrollLeft <= width) {
        el.append(items[0]);
        el.scrollLeft = scrollLeft - width;
    }
}

var lastscroll;
div.addEventListener("scroll", function() {
    var el = this;

    if (lastscroll) {
        clearTimeout(lastscroll);
    }
    lastscroll = setTimeout(function() {
        updateSort(el);
    }, 50);
    setActive(el, nav);
});

// dots state
function setActive(el, nav) {
    var scrollLeft = el.scrollLeft;
    var imgs = el.children;
    var activeimg;
    for (var i = 0; i < imgs.length; i++) {
        if (Math.abs(imgs[i].offsetLeft - scrollLeft) < 50) {
        activeimg = imgs[i];
        }
    }
    if (activeimg) {
        var links = nav.children;
        for (var j = 0; j < links.length; j++) {
        links[j].classList.remove("active");
        }
        var activeA = nav.querySelector("a[href='#" + activeimg.id + "']");
        activeA.classList.add("active");
    }
}

// dots click smooth scroll
nav.addEventListener("click", function(e) {
    var link = e.target.closest("a");
    var matchingImg = div.querySelector(
        "img[id='" + link.getAttribute("href").replace("#", "") + "']"
    );
    e.preventDefault();
    div.scrollTo({ left: matchingImg.offsetLeft, behavior: "smooth" });
});

updateSort(div);
setActive(div, nav);

//

