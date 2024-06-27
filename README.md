O módulo PyDevSup dá suporte a IOC baseadas em EPICS Base, por meio de records
do tipo `Python Device`. Esses records aceitam em seus campos `INP` e `OUT`
links para modulos Python definidos em scripts externos que implementam a lógica
de processamento do record em questão.

Resultado do comando `htop` filtrando o `st.cmd`:

```
    PID USER       PRI  NI  VIRT   RES   SHR S  CPU%▽MEM%   TIME+  Command
 249195 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:07.57 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249197 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249205 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249206 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249207 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249208 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249209 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249210 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249213 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249214 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249215 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249216 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.02 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249217 gustavo.re  20   0 1629M 81216 30548 S   0.6  1.0  0:01.06 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249218 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.09 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249219 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.26 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249220 gustavo.re  20   0 1629M 81216 30548 S   0.6  1.0  0:00.47 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249221 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249222 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249223 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249224 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249225 gustavo.re  20   0 1629M 81216 30548 S   0.6  1.0  0:04.23 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249226 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
 249228 gustavo.re  20   0 1629M 81216 30548 S   0.0  1.0  0:00.00 ../../bin/linux-x86_64/si_ps_conv_fastcorrs ./st.cmd
```

