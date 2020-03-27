const all = document.querySelectorAll('*');

const mapping = {
  "a": "a",
  "b": "b",
  "i": "i",
  "d": "div",
  "q": "q",
  "str": "strong",
  "sub": "sub",
  "sup": "sup",
  "blk": "blockquote",
  "img": "img",
  "important": "important",
  "warning": "warning",
  "figcaption": "figcaption",
  // "script": "script",
  "": "",
}

function replacer(match, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, offset, string) {
  let el;
  if (p1) {
    el = mapping[p1];
  } else {
    el = "span";
  }

  if (el === "img") {
    if (p3 && p5) {
      return `<${el} ${p10}="${p11}" ${p12}="${p13}" ${p14}="${p15}" class="${p3}" id="${p5}">`;
    } else if (p3 && !p5) {
      return `<${el} ${p10}="${p11}" ${p12}="${p13}" ${p14}="${p15}" class="${p3}">`;
    } else if (p5 && !p3) {
      return `<${el} ${p10}="${p11}" ${p12}="${p13}" ${p14}="${p15}" id="${p5}">`;
    } else {
      return `<${el} ${p10}="${p11}" ${p12}="${p13}" ${p14}="${p15}">`;
    }
  } else if (el === "script") {
    p7 = p7.replace("<p>", "");
    p7 = p7.replace("</p>", "");
    return `<script>${p7}</script>`;
  } else {
    if (p3 && p5) {
      return `<${el} class="${p3}" id="${p5}">${p7}</${el}>`;
    } else if (p3 && !p5) {
      return `<${el} class="${p3}">${p7}</${el}>`;
    } else if (p5 && !p3) {
      return `<${el} id="${p5}">${p7}</${el}>`;
    } else {
      return `<${el}>${p7}</${el}>`;
    }
  }
}

for (typeEl in mapping) {
  // /(::)([a-zA-Z0-9_-]*)+(::)([a-zA-Z0-9_ -@]*)(::)(::)/g -> old
  // (:)([a-zA-Z0-9_-]*)+(:)([a-zA-Z0-9_-]*)+(::)([a-zA-Z0-9_ -@]*)(::::) -> newer
  // (:)([a-zA-Z0-9_-]*)*(:)([a-zA-Z0-9_-]*)*(::)([a-zA-Z0-9_ -@][^:]*)(::::) -> newest
  if (typeEl === "img") {
    var regex = `(${typeEl})(:)([a-zA-Z0-9 _-]*)*(:)([a-zA-Z0-9 _-]*)*(::)([^:]*)(::::)({ *(alt|src|title|)="([^"]*)" *(alt|src|title)="([^"]*)" *(alt|src|title)="([^"]*)" *})`; // -> works perfectly (seemingly!)
  } else if (typeEl === "script") {
    var regex = `(${typeEl})(:)([a-zA-Z0-9 _-]*)*(:)([a-zA-Z0-9 _-]*)*(::)((.|\n)*)(::::)`;
  } else {
    var regex = `(${typeEl})(:)([a-zA-Z0-9 _-]*)*(:)([a-zA-Z0-9 _-]*)*(::)(([^:]|\n)*)(::::)`; // -> works perfectly (seemingly!)
  }

  var inlineRE = new RegExp(regex, 'g');

  for (let element of all) {
    if (inlineRE.test(element.innerHTML)) {
      element.innerHTML = element.innerHTML.replace(inlineRE, replacer);
    }
  }
}


const td = document.querySelectorAll('td');

for (let i of td) {
  if (i.innerHTML === '') {
    i.innerHTML = '<i class="fas fa-times"></i>';
  } else if (i.innerHTML === '') {
    i.innerHTML = '<i class="fas fa-check"></i>';
  }
}
