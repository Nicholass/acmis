      
        smile_img = new Image();
        smile_img_new = new Image();

        smile_count = <?php echo $smile_count; ?>;

        var smile_index = new Array();
        var i = <?php echo $smile_index; ?>;
        var limit = <?php echo $smile_limit; ?>;
        while (i <= limit) {
          smile_index[i] = i;
          i++;
        }

        var smilies = new Array();
        var smilies_text = new Array();

        smilies_text.push(<?php
foreach ($smilies as $smile_text => $smile_file) {
  echo '"'.$smile_text.'", ';
}
?>"");

        smilies.push(<?php
foreach ($smilies as $smile_text => $smile_file) {
  echo '"'.$smile_file.'", ';
}
?>"");

        function bbCodePreview(i) {
          if (i != 'none') {
            preview = "URL("+document.getElementById('smile-'+i).src+") no-repeat center center";
            txt = 'Click to insert '+document.getElementById('smile-'+i).alt+' at text cursor.';
          }
          else {
            preview = "none";
            txt = '';
          }
          document.getElementById('pun_bbcode_smile_preview').style.background = preview;
          document.getElementById('pun_bbcode_smile_text').innerHTML = txt;
        }

        function bbCodeToggle(change) {
          var c = <?php echo $smile_index; ?>;
          var limit = <?php echo $smile_limit; ?>;
          while (limit) {
            var changed = eval(smile_index[c]+change);
            if (changed < 0) {
              changed = eval(changed+smile_count);
            } else if (changed > eval(smile_count-1)) {
              changed = eval(changed-smile_count);
            }

            smile_index[c] = changed;

            smile_img_new.src = '<?php echo $base_url; ?>/img/smilies/'+smilies[smile_index[c]];

            if ( !smile_img.src || (smile_img_new.src != smile_img.src) ) {
              document.getElementById('smile-'+c).src = smile_img_new.src;
              document.getElementById('smile-'+c).alt = smilies_text[smile_index[c]];
              limit--;
            }
            c++;
          }
          // This will show you the image index
          //document.getElementById('pun_bbcode_smile_text').innerHTML = change+' :: '+smile_index[0]+' : '+smile_index[1]+' : '+smile_index[2]+' : '+smile_index[3]+' : '+smile_index[4]+' : '+smile_index[5]+' : '+smile_index[6]+' : '+smile_index[7]+' : '+smile_index[8]+' : '+smile_index[9];
        }
      