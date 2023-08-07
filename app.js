
const axios = require("axios");
const cheerio = require("cheerio");

let items = [];
axios
  .get("https://www.allrecipes.com/recipes/235/world-cuisine/middle-eastern/")
  .then((response) => {
    const $ = cheerio.load(response.data);
    // now you can use the Cheerio API to query the DOM
    $("#mntl-taxonomysc-article-list-group_1-0")
      .children()
      .each((index, el) => {
        // console.log("q22");
        // console.log($(el).text());
        // console.log($(el).children().);
        $(el)
          .children()
          .each((index, els) => {
            // console.log("123123", $(els).children().length);
            $(els)
              .children()
              .each((i, m) => {
                // console.log(i, $(m).attr("href"));
                if ($(m).attr("href")) {
                  items.push($(m).attr("href"));
                }
              });
            // console.log(213123213, els, els.children().length);
            // $(els)
            //   .children()
            //   .each(index, (elss) => {
            //     console.log("elss", 21321);
            //   });
            // console.log(els.attributes)
            // console.log($(els).children().attr('href'));
          });
      });
  })
  .then(() => {
    items.map((item) => {
      axios.get(item).then((response) => {
        const $ = cheerio.load(response.data);
        // now you can use the Cheerio API to query the DOM
        console.log(
          "recepie:",
          $("title").text(),
          $("#mntl-structured-ingredients_1-0 > ul").text(),
          $("#mntl-nutrition-facts-label_1-0").text(),
          "end of reccepie"
        );
      });
    });
  })
  .catch(console.error);
