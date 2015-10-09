#! /bin/bash

if [[ ! -n "${1}" ]]; then
  echo "There is no argument"
  exit 3
fi

tmpfile=`mktemp`

cmd="grep \"status_code:200\" ${1} | awk -F \"\t\" 'match(\$1, /.*\[(.*)\+0900/, time) && match(\$7, /.*\:(.*)/, rectime) {print time[1],rectime[1]}' | sort -n"

eval ${cmd} > ${tmpfile}

cmd="cat ${tmpfile} | awk '{print \$1}' | uniq"
times=`eval ${cmd}`

for i in ${times}
do
  num=`grep ${i} ${tmpfile} -c`
  reqsec=`grep ${i} ${tmpfile} | awk '{print \$2}'`

  unset reqsec_sum
  for j in ${reqsec}
  do
    reqsec_sum=`expr ${reqsec_sum} + ${j}`
  done

  unset reqsec_ave
  reqsec_ave=`expr ${reqsec_sum} / ${num}`

  echo "${i} ${reqsec_ave}"
done

rm -f ${tmpfile}
