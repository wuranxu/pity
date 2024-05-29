(self.webpackChunkpity=self.webpackChunkpity||[]).push([[3807],{41612:function(T,Z,e){T=e.nmd(T);var r=e(52677).default;ace.define("ace/theme/material-one-dark",["require","exports","module","ace/lib/dom"],function(v,E,j){E.isDark=!1,E.cssClass="ace-material-one-dark",E.cssText=`
.ace-material-one-dark .ace_gutter {
  background: #272B33;
  color: rgb(103,111,122)
}

.ace-material-one-dark .ace_print-margin {
  // width: 1px;
  background: #e8e8e8
}

.ace-material-one-dark {
  background-color: #272B33;
  color: #A6B2C0
}

.ace-material-one-dark .ace_cursor {
  color: #528BFF
}

.ace-material-one-dark .ace_marker-layer .ace_selection {
  background: #3D4350
}

.ace-material-one-dark.ace_multiselect .ace_selection.ace_start {
  box-shadow: 0 0 3px 0px #272B33;
  border-radius: 2px
}

.ace-material-one-dark .ace_marker-layer .ace_step {
  background: rgb(198, 219, 174)
}

.ace-material-one-dark .ace_marker-layer .ace_bracket {
  margin: -1px 0 0 -1px;
  border: 1px solid #747369
}

.ace-material-one-dark .ace_marker-layer .ace_active-line {
  background: #2B313A
}

.ace-material-one-dark .ace_gutter-active-line {
  background-color: #2B313A
}

.ace-material-one-dark .ace_marker-layer .ace_selected-word {
  border: 1px solid #3D4350
}

.ace-material-one-dark .ace_fold {
  background-color: #61AEEF;
  border-color: #A6B2C0
}

.ace-material-one-dark .ace_keyword {
  color: #C679DD
}

.ace-material-one-dark .ace_keyword.ace_operator {
  color: #A6B2C0
}

.ace-material-one-dark .ace_keyword.ace_other.ace_unit {
  color: #D2945D
}

.ace-material-one-dark .ace_constant {
  color: #D2945D
}

.ace-material-one-dark .ace_constant.ace_numeric {
  color: #D2945D
}

.ace-material-one-dark .ace_constant.ace_character.ace_escape {
  color: #57B6C2
}

.ace-material-one-dark .ace_support.ace_function {
  color: #57B6C2
}

.ace-material-one-dark .ace_support.ace_class {
  color: #E5C17C
}

.ace-material-one-dark .ace_storage {
  color: #C679DD
}

.ace-material-one-dark .ace_invalid.ace_illegal {
  color: #272B33;
  background-color: #f2777a
}

.ace-material-one-dark .ace_invalid.ace_deprecated {
  color: #272B33;
  background-color: #d27b53
}

.ace-material-one-dark .ace_string {
  color: #90C378
}

.ace-material-one-dark .ace_string.ace_regexp {
  color: #57B6C2
}

.ace-material-one-dark .ace_comment {
  font-style: italic;
  color: #59626F
}

.ace-material-one-dark .ace_variable {
  color: #DF6A73
}

.ace-material-one-dark .ace_meta.ace_selector {
  color: #C679DD
}

.ace-material-one-dark .ace_entity.ace_other.ace_attribute-name {
  color: #D2945D
}

.ace-material-one-dark .ace_entity.ace_name.ace_function {
  color: #61AEEF
}

.ace-material-one-dark .ace_entity.ace_name.ace_tag {
  color: #DF6A73
}

.ace-material-one-dark .ace_markup.ace_list {
  color: #DF6A73
}
`;var I=v("ace/lib/dom");I.importCssString(E.cssText,E.cssClass)}),function(){ace.require(["ace/theme/ace-material-one-dark"],function(v){r(T)=="object"&&r(Z)=="object"&&T&&(T.exports=v)})}()},26194:function(T,Z,e){"use strict";e.d(Z,{Z:function(){return le}});var r=e(12444),v=e.n(r),E=e(72004),j=e.n(E),I=e(31996),O=e.n(I),h=e(26037),D=e.n(h),o=e(67294),L=e(53239),b=e.n(L),k=e(74981),c=e(82679),P=e.n(c),s=e(5619),R=e.n(s),oe=e(41612),w=e.n(oe),_=e(90252),pe=e.n(_),Y=e(85893),le=function(ie){O()(U,ie);var ce=D()(U);function U(){return v()(this,U),ce.apply(this,arguments)}return j()(U,[{key:"componentDidMount",value:function(){var n=this;this.props.setEditor(this.refs),(0,c.addCompleter)({getCompletions:function(z,ee,V,te,t){t(null,(n.props.tables||[]).map(function(H){return{name:H,value:H}}))}})}},{key:"render",value:function(){var n=this.props,q=n.value,z=n.onChange,ee=n.height,V=n.readOnly,te=n.theme;return(0,Y.jsx)(k.ZP,{ref:"aceEditor",mode:"json",theme:te||"material-one-dark",fontSize:14,showGutter:!0,showPrintMargin:!1,onChange:z,value:q,wrapEnabled:!0,highlightActiveLine:!0,enableSnippets:!0,style:{width:"100%",height:ee||300},setOptions:{readOnly:V||!1,enableBasicAutocompletion:!0,enableLiveAutocompletion:!0,enableSnippets:!0,showLineNumbers:!0,tabSize:4,useWorker:!0}})}}]),U}(o.Component)},37594:function(T,Z,e){"use strict";e.d(Z,{B:function(){return E}});var r=e(91321),v="//at.alicdn.com/t/font_915840_2b8lahxt5xv.js",E=(0,r.Z)({scriptUrl:v})},56262:function(T,Z,e){"use strict";e.d(Z,{Z:function(){return H}});var r=e(67294),v=e(34041),E=e(55102),j=e(71230),I=e(15746),O=e(15009),h=e.n(O),D=e(19632),o=e.n(D),L=e(99289),b=e.n(L),k=e(5574),c=e.n(k),P=e(97857),s=e.n(P),R=e(13769),oe=e.n(R),w=e(8232),_=e(2453),pe=e(86738),Y=e(96746),le=e(96074),ie=e(14726),ce=e(72051),U=e(51042),de=e(19478),n=e(85893),q=["editing","dataIndex","title","type","setType","record","index","key","children"],z=v.Z.Option,ee=function(d){var F=d.editing,K=d.dataIndex,$=d.title,ne=d.type,B=d.setType,m=d.record,ue=d.index,ve=d.key,N=d.children,X=oe()(d,q);return(0,n.jsx)("td",s()(s()({},X),{},{children:F?(0,n.jsx)(w.Z.Item,{name:K,style:{margin:0},initialValue:m.dataIndex,rules:[{required:!0,message:"Please Input ".concat($,"!")}],children:(0,n.jsx)(E.Z,{placeholder:"please input ".concat($)})}):N}))},V=function(d){var F=d.data,K=d.setData,$=d.ossFileList,ne=w.Z.useForm(),B=c()(ne,1),m=B[0],ue=(0,r.useState)(""),ve=c()(ue,2),N=ve[0],X=ve[1],xe=(0,r.useState)("FILE"),J=c()(xe,2),G=J[0],he=J[1],Ee=(0,r.useState)(null),je=c()(Ee,2),Q=je[0],Ce=je[1],me=function(f){return f.key===N},De=function(f){m.setFieldsValue(s()({},f)),X(f.key)},Se=function(){X("")},Oe=function(){var C=b()(h()().mark(function f(l){var p,g,re,se,be;return h()().wrap(function(x){for(;;)switch(x.prev=x.next){case 0:return x.prev=0,x.next=3,m.validateFields();case 3:if(p=x.sent,!(G==="FILE"&&!Q)){x.next=7;break}return _.ZP.info("\u8BF7\u9009\u62E9\u6587\u4EF6"),x.abrupt("return");case 7:if(g=o()(F),re=g.findIndex(function(ge){return l===ge.key}),!(re>-1)){x.next=20;break}if(se=g[re],be=g.findIndex(function(ge){return p.key===ge.key}),!(be>-1)){x.next=15;break}return _.ZP.info("\u8BE5key\u5DF2\u5B58\u5728"),x.abrupt("return");case 15:g.splice(re,1,s()(s()(s()({},se),p),{},{type:G,value:Q})),K(g),X(""),x.next=23;break;case 20:g.push(s()(s()({},p),{},{type:G,value:Q})),K(g),X("");case 23:x.next=28;break;case 25:x.prev=25,x.t0=x.catch(0),console.log("Validate Failed:",x.t0);case 28:case"end":return x.stop()}},f,null,[[0,25]])}));return function(l){return C.apply(this,arguments)}}(),Te=function(f){var l=o()(F);l.splice(l.findIndex(function(p){return f===p.key}),1),K(l)},fe=[{title:"KEY",dataIndex:"key",width:"30%",editable:!0},{title:"TYPE",dataIndex:"type",type:"select",width:"10%",render:function(f,l){return l.key===N?(0,n.jsxs)(v.Z,{style:{width:"100%"},value:G,onChange:function(g){he(g)},children:[(0,n.jsx)(z,{value:"FILE",children:"FILE"}),(0,n.jsx)(z,{value:"TEXT",children:"TEXT"})]}):l.type}},{title:"VALUE",dataIndex:"value",width:"40%",render:function(f,l){return l.key===N?G==="FILE"?(0,n.jsx)(v.Z,{style:{width:"100%"},placeholder:"please select oss file",showSearch:!0,value:Q,onChange:function(g){return Ce(g)},children:$.map(function(p){return(0,n.jsx)(z,{value:p.file_path,children:p.file_path},p.file_path)})}):(0,n.jsx)(E.Z,{placeholder:"please input VALUE",value:Q,onChange:function(g){Ce(g.target.value)}}):G==="FILE"?(0,n.jsx)("a",{href:"".concat(de.Z.URL,"/oss/download?filepath=").concat(l.value),children:l.value}):l.value}},{title:"OPERATION",dataIndex:"operation",render:function(f,l){var p=me(l);return p?(0,n.jsxs)("span",{children:[(0,n.jsx)("a",{onClick:function(){return Oe(l.key)},style:{marginRight:8},children:"Save"}),(0,n.jsx)(pe.Z,{title:"Sure to cancel?",onConfirm:Se,children:(0,n.jsx)("a",{children:"Cancel"})})]}):(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(Y.Z.Link,{disabled:N!=="",onClick:function(){return De(l)},children:"Edit"}),(0,n.jsx)(le.Z,{type:"vertical"}),(0,n.jsx)(Y.Z.Link,{disabled:N!=="",onClick:function(){return Te(l.key)},children:"Remove"})]})}}],ae=function(){var f=[].concat(o()(F),[{key:"",type:"TEXT",value:null}]);K(f),he("FILE")},Ze=fe.map(function(C){return C.editable?s()(s()({},C),{},{onCell:function(l,p){return{record:l,index:p,type:G,setType:he,dataIndex:C.dataIndex,title:C.title,editing:me(l)}}}):C});return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(j.Z,{style:{marginBottom:12},children:(0,n.jsx)(I.Z,{span:6,children:(0,n.jsx)(ie.ZP,{type:"primary",onClick:ae,icon:(0,n.jsx)(U.Z,{}),children:"Add"})})}),(0,n.jsx)(w.Z,{form:m,component:!1,children:(0,n.jsx)(ce.Z,{components:{body:{cell:ee}},dataSource:F,columns:Ze,rowClassName:"editable-row",pagination:{onChange:Se}})})]})},te=V,t=v.Z.Option,H=function(M){var d=M.ossFileList,F=M.dataSource,K=M.setDataSource,$=[{title:"KEY",dataIndex:"key",render:function(){return(0,n.jsx)(E.Z,{})}},{title:"VALUE",dataIndex:"value",render:function(){return(0,n.jsx)(v.Z,{children:d.map(function(B){return(0,n.jsx)(t,{value:B.key,children:B.key},B.key)})})}}];return(0,n.jsx)(j.Z,{gutter:8,style:{marginTop:16},children:(0,n.jsx)(I.Z,{span:24,children:(0,n.jsx)(te,{bordered:!0,columns:$,data:F,setData:K,ossFileList:d})})})}},53677:function(T,Z,e){"use strict";var r=e(67294),v=e(69935),E=e(85893);Z.Z=function(j){var I=j.columns,O=j.dataSource,h=j.title,D=j.setDataSource,o=j.editableKeys,L=j.setEditableRowKeys,b=j.extra;return(0,r.useEffect)(function(){L(O.map(function(k){return k.id}))},[O]),(0,E.jsx)(v.Z,{headerTitle:h,columns:I,rowKey:"id",value:O,onChange:D,recordCreatorProps:{newRecordType:"dataSource",record:function(){return{id:Date.now()}}},editable:{type:"multiple",editableKeys:o,actionRender:function(c,P,s){return[s.delete]},onValuesChange:function(c,P){b&&b(P),D(P)},onChange:L}})}},26969:function(T,Z,e){"use strict";e.r(Z),e.d(Z,{default:function(){return ne}});var r=e(67294),v=e(52677),E=e.n(v),j=e(15009),I=e.n(j),O=e(99289),h=e.n(O),D=e(5574),o=e.n(D),L=e(34041),b=e(11941),k=e(16568),c=e(50136),P=e(71230),s=e(15746),R=e(4393),oe=e(55102),w=e(14726),_=e(78045),pe=e(85418),Y=e(72051),le=e(65987),ie=e(31484),ce=e(34804),U=e(53677),de=e(12414),n=e(90596),q=e(10981),z=e(56262),ee=e(37594),V=e(26194),te=e(58841),t=e(85893),H=L.Z.Option,M=b.Z.TabPane,d={200:{color:"#67C23A",text:"OK"},401:{color:"#F56C6C",text:"unauthorized"},400:{color:"#F56C6C",text:"Bad Request"}},F=function(m){return m&&m.response?(0,t.jsx)("div",{style:{marginRight:16},children:(0,t.jsxs)("span",{children:["Status:",(0,t.jsxs)("span",{style:{color:d[m.status_code]?d[m.status_code].color:"#F56C6C",marginLeft:8,marginRight:8},children:[m.status_code," ",d[m.status_code]?d[m.status_code].text:""]}),(0,t.jsxs)("span",{style:{marginLeft:8,marginRight:8},children:["Time: ",(0,t.jsx)("span",{style:{color:"#67C23A"},children:m.cost})]})]})}):null},K=function(m){var ue=m.loading,ve=m.gconfig,N=m.dispatch,X=(0,r.useState)(0),xe=o()(X,2),J=xe[0],G=xe[1],he=(0,r.useState)("JSON"),Ee=o()(he,2),je=Ee[0],Q=Ee[1],Ce=(0,r.useState)("GET"),me=o()(Ce,2),De=me[0],Se=me[1],Oe=(0,r.useState)([]),Te=o()(Oe,2),fe=Te[0],ae=Te[1],Ze=(0,r.useState)([]),C=o()(Ze,2),f=C[0],l=C[1],p=(0,r.useState)(function(){return fe.map(function(u){return u.id})}),g=o()(p,2),re=g[0],se=g[1],be=(0,r.useState)(function(){return f.map(function(u){return u.id})}),Ie=o()(be,2),x=Ie[0],ge=Ie[1],Ye=(0,r.useState)(null),ke=o()(Ye,2),Le=ke[0],Ve=ke[1],Qe=(0,r.useState)(!1),_e=o()(Qe,2),we=_e[0],Me=_e[1],qe=(0,r.useState)({}),Ae=o()(qe,2),A=Ae[0],et=Ae[1],tt=(0,r.useState)([]),Re=o()(tt,2),Be=Re[0],nt=Re[1],at=(0,r.useState)(null),Ue=o()(at,2),yt=Ue[0],Fe=Ue[1],rt=ve.ossFileList,st=(0,r.useState)(""),Ke=o()(st,2),Pe=Ke[0],We=Ke[1],ot=(0,t.jsxs)(L.Z,{value:De,onChange:function(a){return Se(a)},style:{width:120,fontSize:16,textAlign:"left"},children:[(0,t.jsx)(H,{value:"GET",children:"GET"},"GET"),(0,t.jsx)(H,{value:"POST",children:"POST"},"POST"),(0,t.jsx)(H,{value:"PUT",children:"PUT"},"PUT"),(0,t.jsx)(H,{value:"DELETE",children:"DELETE"},"DELETE")]}),He=[{title:"KEY",dataIndex:"key",key:"key"},{title:"VALUE",dataIndex:"value",key:"value"}],Ne=function(a){if(A[a]===null||A[a]===void 0||A[a]==="{}")return[];var i=JSON.parse(A[a]);return Object.keys(i).map(function(y){return{key:y,value:i[y]}})},Je=function(a){var i=Pe.split("?")[0];a.forEach(function(y,W){y.key&&(W===0?i="".concat(i,"?").concat(y.key,"=").concat(y.value||""):i="".concat(i,"&").concat(y.key,"=").concat(y.value||""))}),We(i)},lt=function(a){var i=a.split("?");if(i.length<2)ae([]);else{var y=i[1].split("&"),W=[],S=[];y.forEach(function(ht,ze){var mt=ht.split("="),$e=o()(mt,2),ft=$e[0],gt=$e[1],Xe=Date.now();S.push(Xe+ze+10),W.push({key:ft,value:gt,id:Xe+ze+10,description:""})}),ae(W),se(S)}},ye=function(a){Q(a)},it=function(){var a={};return f.forEach(function(i){i.key!==""&&(a[i.key]=i.value)}),a},ct=function(){var u=h()(I()().mark(function a(){var i,y;return I()().wrap(function(S){for(;;)switch(S.prev=S.next){case 0:if(Pe!==""){S.next=3;break}return k.ZP.error({message:"\u8BF7\u6C42Url\u4E0D\u80FD\u4E3A\u7A7A"}),S.abrupt("return");case 3:return Me(!0),i={method:De,url:Pe,body:J===2?JSON.stringify(Be):Le,body_type:J,headers:it()},J===0&&(i.body=null),S.next=8,(0,de.c3)(i);case 8:y=S.sent,Me(!1),q.Z.response(y,!0)&&et(y.data);case 11:case"end":return S.stop()}},a)}));return function(){return u.apply(this,arguments)}}(),dt=function(a,i){if(a==="params"){var y=fe.filter(function(S){return S.id!==i});ae(y),Je(y)}else{var W=f.filter(function(S){return S.id!==i});l(W)}},ut=(0,t.jsxs)(c.Z,{children:[(0,t.jsx)(c.Z.Item,{children:(0,t.jsx)("a",{onClick:function(){ye("Text")},children:"Text"})},"Text"),(0,t.jsx)(c.Z.Item,{children:(0,t.jsx)("a",{onClick:function(){ye("JavaScript")},children:"JavaScript"})},"JavaScript"),(0,t.jsx)(c.Z.Item,{children:(0,t.jsx)("a",{onClick:function(){ye("JSON")},children:"JSON"})},"JSON"),(0,t.jsx)(c.Z.Item,{children:(0,t.jsx)("a",{onClick:function(){ye("HTML")},children:"HTML"})},"HTML"),(0,t.jsx)(c.Z.Item,{children:(0,t.jsx)("a",{onClick:function(){ye("XML")},children:"XML"})},"XML")]}),Ge=function(a){return[{title:"KEY",key:"key",dataIndex:"key"},{title:"VALUE",key:"value",dataIndex:"value"},{title:"DESCRIPTION",key:"description",dataIndex:"description"},{title:"\u64CD\u4F5C",valueType:"option",render:function(y,W){return(0,t.jsxs)(t.Fragment,{children:[(0,t.jsx)(le.Z,{style:{cursor:"pointer"},onClick:function(){se([W.id])}}),(0,t.jsx)(ie.Z,{style:{cursor:"pointer",marginLeft:8},onClick:function(){dt(a,W.id)},twoToneColor:"#eb2f96"})]})}}]},vt=function(a){return a===0?(0,t.jsx)("div",{style:{height:"20vh",lineHeight:"20vh",textAlign:"center"},children:"This request does not have a body"}):a===2?(0,t.jsx)(z.Z,{ossFileList:rt,dataSource:Be,setDataSource:nt}):(0,t.jsx)(P.Z,{style:{marginTop:12},children:(0,t.jsx)(s.Z,{span:24,children:(0,t.jsx)(R.Z,{bodyStyle:{padding:0},children:(0,t.jsx)(V.Z,{value:Le,onChange:function(y){return Ve(y)},height:"20vh",setEditor:Fe})})})})};return(0,t.jsx)(te._z,{title:"\u5728\u7EBFHTTP\u6D4B\u8BD5\u5DE5\u5177",breadcrumb:null,children:(0,t.jsxs)(R.Z,{children:[(0,t.jsxs)(P.Z,{gutter:[8,8],children:[(0,t.jsx)(s.Z,{span:18,children:(0,t.jsx)(oe.Z,{size:"large",value:Pe,addonBefore:ot,placeholder:"\u8BF7\u8F93\u5165\u8981\u8BF7\u6C42\u7684url",onChange:function(a){We(a.target.value),lt(a.target.value)}})}),(0,t.jsx)(s.Z,{span:6,children:(0,t.jsxs)(w.ZP,{onClick:ct,loading:we,type:"primary",size:"large",style:{marginRight:16,float:"right"},children:[(0,t.jsx)(ee.B,{type:"icon-fasong1"}),"Send"," "]})})]}),(0,t.jsx)(P.Z,{style:{marginTop:8},children:(0,t.jsxs)(b.Z,{defaultActiveKey:"1",style:{width:"100%"},children:[(0,t.jsx)(M,{tab:"Params",children:(0,t.jsx)(U.Z,{columns:Ge("params"),title:"Query Params",dataSource:fe,setDataSource:ae,extra:Je,editableKeys:re,setEditableRowKeys:se})},"1"),(0,t.jsx)(M,{tab:"Headers",children:(0,t.jsx)(U.Z,{columns:Ge("headers"),title:"Headers",dataSource:f,setDataSource:l,editableKeys:x,setEditableRowKeys:ge})},"2"),(0,t.jsxs)(M,{tab:"Body",children:[(0,t.jsxs)(P.Z,{children:[(0,t.jsxs)(_.ZP.Group,{defaultValue:0,value:J,onChange:function(a){G(a.target.value),a.target.value===2&&N({type:"gconfig/listOssFile"})},children:[(0,t.jsx)(_.ZP,{value:0,children:"none"}),(0,t.jsx)(_.ZP,{value:2,children:"form-data"}),(0,t.jsx)(_.ZP,{value:3,children:"x-www-form-urlencoded"}),(0,t.jsx)(_.ZP,{value:1,children:"raw"}),(0,t.jsx)(_.ZP,{value:4,children:"binary"}),(0,t.jsx)(_.ZP,{value:5,children:"GraphQL"})]}),J===1?(0,t.jsx)(pe.Z,{style:{marginLeft:8},overlay:ut,trigger:["click"],children:(0,t.jsxs)("a",{onClick:function(a){return a.preventDefault()},children:[je," ",(0,t.jsx)(ce.Z,{})]})}):null]}),vt(J)]},"3")]})}),(0,t.jsx)(P.Z,{gutter:[8,8],children:Object.keys(A).length===0?null:(0,t.jsxs)(b.Z,{style:{width:"100%"},tabBarExtraContent:F(A),children:[(0,t.jsx)(M,{tab:"Body",children:(0,t.jsx)(V.Z,{readOnly:!0,setEditor:Fe,language:A.response&&A.response_headers.indexOf("json")>-1?"json":"text",value:A.response&&E()(A.response)==="object"?JSON.stringify(A.response,null,2):A.response||"",height:"30vh"})},"1"),(0,t.jsx)(M,{tab:"Cookie",children:(0,t.jsx)(Y.Z,{columns:He,dataSource:Ne("cookies"),size:"small",pagination:!1})},"2"),(0,t.jsx)(M,{tab:"Headers",children:(0,t.jsx)(Y.Z,{columns:He,dataSource:Ne("response_headers"),size:"small",pagination:!1})},"3")]})})]})})},$=(0,n.connect)(function(B){var m=B.loading,ue=B.gconfig;return{loading:m,gconfig:ue}})(K),ne=function(){return(0,t.jsx)($,{})}},5619:function(T,Z,e){T=e.nmd(T),ace.define("ace/ext/spellcheck",["require","exports","module","ace/lib/event","ace/editor","ace/config"],function(r,v,E){"use strict";var j=r("../lib/event");v.contextMenuHandler=function(O){var h=O.target,D=h.textInput.getElement();if(!!h.selection.isEmpty()){var o=h.getCursorPosition(),L=h.session.getWordRange(o.row,o.column),b=h.session.getTextRange(L);if(h.session.tokenRe.lastIndex=0,!!h.session.tokenRe.test(b)){var k="",c=b+" "+k;D.value=c,D.setSelectionRange(b.length,b.length+1),D.setSelectionRange(0,0),D.setSelectionRange(0,b.length);var P=!1;j.addListener(D,"keydown",function s(){j.removeListener(D,"keydown",s),P=!0}),h.textInput.setInputHandler(function(s){if(s==c)return"";if(s.lastIndexOf(c,0)===0)return s.slice(c.length);if(s.substr(D.selectionEnd)==c)return s.slice(0,-c.length);if(s.slice(-2)==k){var R=s.slice(0,-2);if(R.slice(-1)==" ")return P?R.substring(0,D.selectionEnd):(R=R.slice(0,-1),h.session.replace(L,R),"")}return s})}}};var I=r("../editor").Editor;r("../config").defineOptions(I.prototype,"editor",{spellcheck:{set:function(O){var h=this.textInput.getElement();h.spellcheck=!!O,O?this.on("nativecontextmenu",v.contextMenuHandler):this.removeListener("nativecontextmenu",v.contextMenuHandler)},value:!0}})}),function(){ace.require(["ace/ext/spellcheck"],function(r){T&&(T.exports=r)})}()}}]);
