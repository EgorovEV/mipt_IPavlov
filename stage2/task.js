exports.Task = extend(TolokaHandlebarsTask, function (options) {
  TolokaHandlebarsTask.call(this, options);
}, {onRender: function() {

  var input = this.getTask().input_values.input;
	var words = input.split(' ');
  var task_id = this.getTask().id;

  var task_obj = this;

  var prev_outputs = task_obj.getSolution().output_values;

  // results are stored as array of 2-element arrays
  var selections = [];

  // try to restore prev results so we can analyse results in Toloka GUI
  if (prev_outputs.hasOwnProperty("output")) {
    console.dir(JSON.parse(prev_outputs.output));
    selections = JSON.parse(prev_outputs.output).selections;
    console.log(selections);
  }

  // we will need a reference to a task object
  var task_div = this._element.getElementsByClassName("tagger")[0];

  function report(selections, words){
      var rep = [];
      var next_id = 0;
      for (var i=0; i<selections.length; i++){
          var sl = selections[i][0];
          var sr = selections[i][1];

          // add all words before the selection
          for (next_id; next_id<sl; next_id++){
              console.dir(next_id);
            	console.dir(words);
            	console.dir(rep);
              rep.push([words[next_id], "o"]);
          }

          // add all words of the selection
          var has_beginning = false;
          for (next_id; next_id < sr+1; next_id++){
              var tg = has_beginning ? 'i' : 'b';
              has_beginning = true;
              rep.push([words[next_id], tg]);
          }
      }
      // add remaining words after all selections
      for(next_id; next_id < words.length; next_id++) {
          rep.push([words[next_id], "o"]);
      }
      return rep;
  }

  function write_answer(selections, words) {
	  task_obj.setSolution({
    	"task_id": task_id,
    	"output_values": {
        "output": JSON.stringify({bio: report(selections, words),
                               selections: selections})}});
  }

  function selectionCheck (selections, left, right) {
      for (var i=0; i<selections.length; i++)
      {
          var sl = selections[i][0];
          var sr = selections[i][1];

          if (sl <= left && left <=sr && sl <=right && right <= sr)
              return ["inside", [sl, sr]];

          if (sr < left || (sl > right)) continue;

          return ["invalid"];
      }
      return ["valid"];
  }

  function makeSpan(index, text) {
      var span = document.createElement("span");
      span.setAttribute("id", index);
      span.textContent = text;
      span.setAttribute("style", "margin-right: 3px");
      span.setAttribute("style", "margin-left: 3px");
      return span;
  }

  function redraw (root, selections, words) {
      while (root.firstChild)
          {root.removeChild(root.firstChild);}

      var next_id = 0;

      for (var i=0; i<selections.length; i++){
          var sl = selections[i][0];
          var sr = selections[i][1];

          // add all words before the selection
          for (next_id; next_id<sl; next_id++){
              root.appendChild(makeSpan(next_id, words[next_id]));
          }

          // add all words of the selection
          var mark = document.createElement("mark");
          mark.setAttribute("id", sl + "_" + sr);
          for (next_id; next_id < sr+1; next_id++){

              mark.appendChild(makeSpan(next_id, words[next_id]));
          }
          root.appendChild(mark)
      }

      // add remaining words after all selections
      for(next_id; next_id < words.length; next_id++) {
          root.appendChild(makeSpan(next_id, words[next_id]));}
  }

  redraw(task_div, selections, words);

  write_answer(selections, words);

  task_div.onmouseup = function (e) {
      var s = window.getSelection();
      if(s.isCollapsed){
          var r = s.getRangeAt(0);
          var o = r.endContainer.parentElement;

          if (o.parentElement.tagName === 'MARK') {

              var sstr = o.parentElement.id.split('_');
              var c = [parseInt(sstr[0]), parseInt(sstr[1])];
              selections = selections.filter(function (sel) {
                  return sel[0] !== c[0] || sel[1] !== c[1]
              });
              s.removeAllRanges();
            	write_answer(selections, words);
              redraw(e.currentTarget, selections, words);
          }
      } else {
          var r = s.getRangeAt(0);
          var o = r.endContainer.parentElement;

          var left = parseInt(r.startContainer.parentElement.getAttribute("id"));
          var right = parseInt(o.getAttribute("id"));

          if (!isNaN(left) && !isNaN(right)) {
            c = selectionCheck(selections, left, right);

            switch (c[0]) {
                case "invalid":
                    break;
                case "valid":
                    selections.push([left, right]);
                    selections.sort(function (s1, s2) {
                        return s1[0] - s2[0];
                    });
                    break;
                case "inside":
                    selections = selections.filter(function (sel) {
                        return sel[0] !== c[1][0] || sel[1] !== c[1][1]
                    });
                    break;
            }
          }
          s.removeAllRanges();
          write_answer(selections, words);
          redraw(e.currentTarget, selections, words);
      }
  };

  },
  onDestroy: function() {
    // Задание завершено, можно освобождать (если были использованы) глобальные ресурсы
  }
});

function extend(ParentClass, constructorFunction, prototypeHash) {
  constructorFunction = constructorFunction || function () {};
  prototypeHash = prototypeHash || {};
  if (ParentClass) {
    constructorFunction.prototype = Object.create(ParentClass.prototype);
  }
  for (var i in prototypeHash) {
    constructorFunction.prototype[i] = prototypeHash[i];
  }
  return constructorFunction;
}
