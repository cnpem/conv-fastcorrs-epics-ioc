O módulo PyDevSup dá suporte a IOC baseadas em EPICS Base, por meio de records
do tipo `Python Device`. Esses records aceitam em seus campos `INP` e `OUT`
links para modulos Python definidos em scripts externos que implementam a lógica
de processamento do record em questão.

Resultado do comando `htop` filtrando o `st.cmd`:

```
    PID USER       PRI  NI  VIRT   RES   SHR S  CPU%▽MEM%   TIME+  Command
 494078 gustavo.re  20   0 1803M 80836 30140 S   1.9  1.0  0:12.73 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494094 gustavo.re  20   0 1803M 80836 30140 S   1.9  1.0  0:08.92 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494080 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494081 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.06 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494082 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.06 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494083 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.06 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494084 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.07 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494085 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.07 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494086 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.06 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494087 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.06 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494088 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494089 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494090 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494091 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494092 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494093 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494095 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494096 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494097 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494098 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494099 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.01 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494100 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.05 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494101 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.10 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494102 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494103 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494104 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494105 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494106 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:01.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494107 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494108 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:01.20 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 494109 gustavo.re  20   0 1803M 80836 30140 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
```

Jitter médio entre monitoramento de corrente e monitoramento de kicks: 0.33 ms
