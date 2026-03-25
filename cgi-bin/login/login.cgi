#!/bin/perl

#┌─────────────────────────────────
#│ LOG IN v1.5 (2002/06/06)
#│ Copyright(C) Kent Web 2002
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'Login v1.5';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#│ 3. methodプロパティ は POST 専用です
#└─────────────────────────────────
# 【 設置例 】
#
#  public_html / index.html (トップページ等)
#      |
#      +-- cgi-bin / login.cgi  [755]
#                    secret.cgi [644] ... 隠しファイル
#                                       (HTMLの拡張子を.cgi に変更)
#

#============#
#  設定項目  #
#============#

# パスワード（半角英数字）
$pass = 'bemu3731';

# スクリプト名
$script = "./login.cgi";

# 隠しファイル（HTMLの拡張子を .cgi に変える）
# 例 → secret.html だと secret.cgi に変更
#       もし隠しファイルが本来のCGIファイルであれば、http://からURLを指定
$secret = './pass.cgi';

# 認証ページからの戻り先 (index.htmlなど）
$home = "http://park11.wakwak.com/~bassman/index.shtml";

# bodyタグ
$body = '<body bgcolor="#EEEEEE" text="#000000" link="#0000FF" vlink="#800080">';

#============#
#  設定完了  #
#============#

# デコード処理
if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
}
foreach (split(/&/, $buf)) {
	local($key, $val) = split(/=/);
	$val =~ tr/+/ /;
	$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	# セキュリティ対策
	$val =~ s/&/&amp;/g;
	$val =~ s/"/&quot;/g;
	$val =~ s/</&lt;/g;
	$val =~ s/>/&gt;/g;
	$val =~ s/\0//g;

	$in{$key} = $val;
}
if ($in{'pass'} ne "") { &login; }

# 認証画面を表示
&header;
print <<"EOM";
[<a href="$home" target="_top">TOPページに戻る</a>]
<div align="center">
- パスワードを入力し認証ボタンを押してください -<BR>
<BR>
布施高校37期吉田学級「Home Room」は同クラス限定ページとなりました。<BR>
他の関係者の方々、すいません。<BR>
本ページに入るにはパスワードが必要です。<BR>
パスワードを入力し「認証する」をおしてや。<BR>
<BR>
<BR>
<BR>
***** パスワード；半角小文字で***** <BR>
パスワードを忘れた人、知らない人はだいもんまでメールください。<BR>
<form action="$script" method="POST" name="entry">
<table border=3 cellspacing=0 cellpadding=3>
<tr>
  <th>PASSWORD</th>
  <td><input type=password name=pass size=10></td>
</tr>
<tr>
  <th colspan=2><input type=submit value=" 認証する "></th>
</tr>
</table>
</form>
<SCRIPT LANGUAGE="JavaScript">
<!--
self.document.entry.pass.focus();
//-->
</SCRIPT>
<br><br><br>
<!-- 著作権表\示 (削除不可) [ $ver ] -->
<span style="font-size:9pt;font-family:verdana">
- <a href="http://www.kent-web.com" target="_top">Log in</a> -
</span></div>
<script LANGUAGE="JavaScript">
<!--
xx = escape(document.referrer);
yy = "";
for (i = 0; i < xx.length; i++) {
zz = xx.charAt(i);
yy += (zz == "+") ? "%2B" : zz;
}
document.write('<img width=1 height=1 ');
document.write('src="http://park11.wakwak.com/~bassman/cgi-bin/mhacclog.cgi');
document.write('?WG01');
document.write('+login');
document.write('+',yy,'">');
// -->
</script>
</body>
</html>
EOM
exit;

#------------#
#  認証処理  #
#------------#
sub login {
	# 認証エラー表示
	if ($in{'pass'} ne $pass) {
		&header;
		print "<div align='center'><h3>認証エラー</h3>\n";
		print "認証画面に戻って再度パスワードを入力して下さい\n";
		print "<form><input type=button value='前画面に戻る' onClick='history.back()'></form>\n";
		print "</div>\n</body></html>\n";
		exit;
	}

	# ファイル指定が http://からであれば Locaionヘッダでジャンプ
	if ($secret =~ /^http\:\/\//) {
		if ($ENV{'PERLXS'} eq "PerlIS") {
			print "HTTP/1.0 302 Temporary Redirection\r\n";
			print "Content-type: text/html\n";
		}
		print "Location: $secret\n\n";
	} else {
		# 隠しファイルを表示
		unless (-e $secret) {
			&error("隠しファイルのパスが不正です : $secret");
		}
		print "Content-type: text/html\n\n";
		open(IN,"$secret") || &error("Open Error : $secret");
		while (<IN>) { print; }
		close(IN);
	}
	exit;
}

#--------------#
#  エラー処理  #
#--------------#
sub error {
	&header;
	print "<div align='center'><h3>ERROR !</h3>\n";
	print "<font color=red><b>$_[0]</b></font></div\n";
	print "</body></html>\n";
	exit;
}

#--------------#
#  HTMLヘッダ  #
#--------------#
sub header {
	print "Content-type: text/html\n\n";
	print "<html>\n<head>\n";
	print "<META HTTP-EQUIV=\"Content-type\" CONTENT=\"text/html; charset=Shift_JIS\">\n";
	print "<title>認証</title></head>\n";
	print "$body\n";
}

