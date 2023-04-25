// Initialise variables
var pageHtml = '';
var pageURL = '';

// Get the HTML of the current page
function getPageHtml() {
  return document.documentElement.outerHTML;
}

async function start()
{
  // Set the query to the current tab
  let queryOptions = { active: true, lastFocusedWindow: true };
  let [tab] = await chrome.tabs.query(queryOptions);

  // Get the URL of the current tab
  pageURL = tab.url;

  // Get the HTML data of current tab
  await chrome.scripting.executeScript({target: {tabId: tab.id}, func: getPageHtml,}).then(injectionResults => {
    for (const {frameId ,result} of injectionResults) {
      pageHtml = result;
    }
  });
}

async function main(new_code,scale)
{
  // set position in popup.html to inject product links
  var storefront = document.getElementById('storefront');

  // inject product links to the popup.html
  storefront.innerHTML += new_code;

  // initialize the globe
  try {
    TagCanvas.Start('myCanvas','tags',{
      textColour: '#ff0000',
      outlineColour: '#ff00ff',
      frontSelect: true,
      reverse: true,
      depth: 0.8,
      maxSpeed: 0.05,
      imageRadius: "40%",
      imageScale: scale
    }); 
  } catch(e) {
    // something went wrong, hide the canvas container
    document.getElementById('myCanvasContainer').style.display = 'none';
  }
}

start();

function detectSliderRelease()
{
  var slider = document.getElementById("slider");
  
  slider.addEventListener("mouseup", function() {
    TagCanvas.Delete('myCanvas');
	  main('', slider.value)
  });

}
window.onload = detectSliderRelease;