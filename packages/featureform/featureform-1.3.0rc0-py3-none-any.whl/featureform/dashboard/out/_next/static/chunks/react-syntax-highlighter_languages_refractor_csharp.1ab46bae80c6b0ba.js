"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[3318],{61958:function(a){function b(a){!function(a){function b(a,b){return a.replace(/<<(\d+)>>/g,function(a,c){return"(?:"+b[+c]+")"})}function c(a,c,d){return RegExp(b(a,c),d||"")}function d(a,b){for(var c=0;c<b;c++)a=a.replace(/<<self>>/g,function(){return"(?:"+a+")"});return a.replace(/<<self>>/g,"[^\\s\\S]")}var e={type:"bool byte char decimal double dynamic float int long object sbyte short string uint ulong ushort var void",typeDeclaration:"class enum interface record struct",contextual:"add alias and ascending async await by descending from(?=\\s*(?:\\w|$)) get global group into init(?=\\s*;) join let nameof not notnull on or orderby partial remove select set unmanaged value when where with(?=\\s*{)",other:"abstract as base break case catch checked const continue default delegate do else event explicit extern finally fixed for foreach goto if implicit in internal is lock namespace new null operator out override params private protected public readonly ref return sealed sizeof stackalloc static switch this throw try typeof unchecked unsafe using virtual volatile while yield"};function f(a){return"\\b(?:"+a.trim().replace(/ /g,"|")+")\\b"}var g=f(e.typeDeclaration),h=RegExp(f(e.type+" "+e.typeDeclaration+" "+e.contextual+" "+e.other)),i=f(e.typeDeclaration+" "+e.contextual+" "+e.other),j=f(e.type+" "+e.typeDeclaration+" "+e.other),k=d(/<(?:[^<>;=+\-*/%&|^]|<<self>>)*>/.source,2),l=d(/\((?:[^()]|<<self>>)*\)/.source,2),m=/@?\b[A-Za-z_]\w*\b/.source,n=b(/<<0>>(?:\s*<<1>>)?/.source,[m,k]),o=b(/(?!<<0>>)<<1>>(?:\s*\.\s*<<1>>)*/.source,[i,n]),p=/\[\s*(?:,\s*)*\]/.source,q=b(/<<0>>(?:\s*(?:\?\s*)?<<1>>)*(?:\s*\?)?/.source,[o,p]),r=b(/[^,()<>[\];=+\-*/%&|^]|<<0>>|<<1>>|<<2>>/.source,[k,l,p]),s=b(/\(<<0>>+(?:,<<0>>+)+\)/.source,[r]),t=b(/(?:<<0>>|<<1>>)(?:\s*(?:\?\s*)?<<2>>)*(?:\s*\?)?/.source,[s,o,p]),u={keyword:h,punctuation:/[<>()?,.:[\]]/},v=/'(?:[^\r\n'\\]|\\.|\\[Uux][\da-fA-F]{1,8})'/.source,w=/"(?:\\.|[^\\"\r\n])*"/.source,x=/@"(?:""|\\[\s\S]|[^\\"])*"(?!")/.source;a.languages.csharp=a.languages.extend("clike",{string:[{pattern:c(/(^|[^$\\])<<0>>/.source,[x]),lookbehind:!0,greedy:!0},{pattern:c(/(^|[^@$\\])<<0>>/.source,[w]),lookbehind:!0,greedy:!0}],"class-name":[{pattern:c(/(\busing\s+static\s+)<<0>>(?=\s*;)/.source,[o]),lookbehind:!0,inside:u},{pattern:c(/(\busing\s+<<0>>\s*=\s*)<<1>>(?=\s*;)/.source,[m,t]),lookbehind:!0,inside:u},{pattern:c(/(\busing\s+)<<0>>(?=\s*=)/.source,[m]),lookbehind:!0},{pattern:c(/(\b<<0>>\s+)<<1>>/.source,[g,n]),lookbehind:!0,inside:u},{pattern:c(/(\bcatch\s*\(\s*)<<0>>/.source,[o]),lookbehind:!0,inside:u},{pattern:c(/(\bwhere\s+)<<0>>/.source,[m]),lookbehind:!0},{pattern:c(/(\b(?:is(?:\s+not)?|as)\s+)<<0>>/.source,[q]),lookbehind:!0,inside:u},{pattern:c(/\b<<0>>(?=\s+(?!<<1>>|with\s*\{)<<2>>(?:\s*[=,;:{)\]]|\s+(?:in|when)\b))/.source,[t,j,m]),inside:u}],keyword:h,number:/(?:\b0(?:x[\da-f_]*[\da-f]|b[01_]*[01])|(?:\B\.\d+(?:_+\d+)*|\b\d+(?:_+\d+)*(?:\.\d+(?:_+\d+)*)?)(?:e[-+]?\d+(?:_+\d+)*)?)(?:[dflmu]|lu|ul)?\b/i,operator:/>>=?|<<=?|[-=]>|([-+&|])\1|~|\?\?=?|[-+*/%&|^!=<>]=?/,punctuation:/\?\.?|::|[{}[\];(),.:]/}),a.languages.insertBefore("csharp","number",{range:{pattern:/\.\./,alias:"operator"}}),a.languages.insertBefore("csharp","punctuation",{"named-parameter":{pattern:c(/([(,]\s*)<<0>>(?=\s*:)/.source,[m]),lookbehind:!0,alias:"punctuation"}}),a.languages.insertBefore("csharp","class-name",{namespace:{pattern:c(/(\b(?:namespace|using)\s+)<<0>>(?:\s*\.\s*<<0>>)*(?=\s*[;{])/.source,[m]),lookbehind:!0,inside:{punctuation:/\./}},"type-expression":{pattern:c(/(\b(?:default|sizeof|typeof)\s*\(\s*(?!\s))(?:[^()\s]|\s(?!\s)|<<0>>)*(?=\s*\))/.source,[l]),lookbehind:!0,alias:"class-name",inside:u},"return-type":{pattern:c(/<<0>>(?=\s+(?:<<1>>\s*(?:=>|[({]|\.\s*this\s*\[)|this\s*\[))/.source,[t,o]),inside:u,alias:"class-name"},"constructor-invocation":{pattern:c(/(\bnew\s+)<<0>>(?=\s*[[({])/.source,[t]),lookbehind:!0,inside:u,alias:"class-name"},"generic-method":{pattern:c(/<<0>>\s*<<1>>(?=\s*\()/.source,[m,k]),inside:{function:c(/^<<0>>/.source,[m]),generic:{pattern:RegExp(k),alias:"class-name",inside:u}}},"type-list":{pattern:c(/\b((?:<<0>>\s+<<1>>|record\s+<<1>>\s*<<5>>|where\s+<<2>>)\s*:\s*)(?:<<3>>|<<4>>|<<1>>\s*<<5>>|<<6>>)(?:\s*,\s*(?:<<3>>|<<4>>|<<6>>))*(?=\s*(?:where|[{;]|=>|$))/.source,[g,n,m,t,h.source,l,/\bnew\s*\(\s*\)/.source]),lookbehind:!0,inside:{"record-arguments":{pattern:c(/(^(?!new\s*\()<<0>>\s*)<<1>>/.source,[n,l]),lookbehind:!0,greedy:!0,inside:a.languages.csharp},keyword:h,"class-name":{pattern:RegExp(t),greedy:!0,inside:u},punctuation:/[,()]/}},preprocessor:{pattern:/(^[\t ]*)#.*/m,lookbehind:!0,alias:"property",inside:{directive:{pattern:/(#)\b(?:define|elif|else|endif|endregion|error|if|line|nullable|pragma|region|undef|warning)\b/,lookbehind:!0,alias:"keyword"}}}});var y=w+"|"+v,z=b(/\/(?![*/])|\/\/[^\r\n]*[\r\n]|\/\*(?:[^*]|\*(?!\/))*\*\/|<<0>>/.source,[y]),A=d(b(/[^"'/()]|<<0>>|\(<<self>>*\)/.source,[z]),2),B=/\b(?:assembly|event|field|method|module|param|property|return|type)\b/.source,C=b(/<<0>>(?:\s*\(<<1>>*\))?/.source,[o,A]);a.languages.insertBefore("csharp","class-name",{attribute:{pattern:c(/((?:^|[^\s\w>)?])\s*\[\s*)(?:<<0>>\s*:\s*)?<<1>>(?:\s*,\s*<<1>>)*(?=\s*\])/.source,[B,C]),lookbehind:!0,greedy:!0,inside:{target:{pattern:c(/^<<0>>(?=\s*:)/.source,[B]),alias:"keyword"},"attribute-arguments":{pattern:c(/\(<<0>>*\)/.source,[A]),inside:a.languages.csharp},"class-name":{pattern:RegExp(o),inside:{punctuation:/\./}},punctuation:/[:,]/}}});var D=/:[^}\r\n]+/.source,E=d(b(/[^"'/()]|<<0>>|\(<<self>>*\)/.source,[z]),2),F=b(/\{(?!\{)(?:(?![}:])<<0>>)*<<1>>?\}/.source,[E,D]),G=d(b(/[^"'/()]|\/(?!\*)|\/\*(?:[^*]|\*(?!\/))*\*\/|<<0>>|\(<<self>>*\)/.source,[y]),2),H=b(/\{(?!\{)(?:(?![}:])<<0>>)*<<1>>?\}/.source,[G,D]);function I(b,d){return{interpolation:{pattern:c(/((?:^|[^{])(?:\{\{)*)<<0>>/.source,[b]),lookbehind:!0,inside:{"format-string":{pattern:c(/(^\{(?:(?![}:])<<0>>)*)<<1>>(?=\}$)/.source,[d,D]),lookbehind:!0,inside:{punctuation:/^:/}},punctuation:/^\{|\}$/,expression:{pattern:/[\s\S]+/,alias:"language-csharp",inside:a.languages.csharp}}},string:/[\s\S]+/}}a.languages.insertBefore("csharp","string",{"interpolation-string":[{pattern:c(/(^|[^\\])(?:\$@|@\$)"(?:""|\\[\s\S]|\{\{|<<0>>|[^\\{"])*"/.source,[F]),lookbehind:!0,greedy:!0,inside:I(F,E)},{pattern:c(/(^|[^@\\])\$"(?:\\.|\{\{|<<0>>|[^\\"{])*"/.source,[H]),lookbehind:!0,greedy:!0,inside:I(H,G)}],char:{pattern:RegExp(v),greedy:!0}}),a.languages.dotnet=a.languages.cs=a.languages.csharp}(a)}a.exports=b,b.displayName="csharp",b.aliases=["dotnet","cs"]}}])