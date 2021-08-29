# prskBorderRetrievalTool
## TOC
 * [Summary](#summary)
 * [Build](#build)
 * [Usage](#usage)
 * [Output](#output)
	 * [retrieve_border](#retrieve_border)
	 * [gen_top3_border](#gen_top3_border)
	 * [FAQ](#faq)

## Summary
This repository contains two programs that get the borders of the Project Sekai rankings.

| Name               | Description                                                 |
| ------------------ | ----------------------------------------------------------- |
| retrieve_border.py | Get the transition of event points for each reward boundary |
| gen_top3_border.py | Get the top 3 event point transitions by user basis.        |

## Build
The program in this repository uses three external libraries. Use the requirements.txt file to install the library.

```shell
pip install -r requirements.txt
```

## Usage
The two programs share the same usage instructions. If you run the program with no arguments, it displays a GUI where you can enter the event_id. Enter the number of the event you want to retrieve as an integer, where event_id is a sequential number starting from 1.  
When the event_id is submitted, the event_point transition is retrieved via the API. The acquired transition data will be output to the 'output' directory in csv format.  

Also, if you set event_point as the argument as follows, you can get the transition without using the GUI.

```shell
$ python retrieve_border.py 4
```

For example, in PowerShell, you can also use the for statement to get the transition in bulk.

```powershell
for ($i=1; $i -lt 33; $i++){
  python gen_top3_border.py $i
}
```

## Output
### retrieve_border
The transition of the event points will be output to `. /output/{event_id}_border.csv/`. The format is as follows.

```csv
datetime,TOP1,TOP2,TOP3,...,TOP100000
2020-10-20 07:30:58,660899,653525,628688,...,5131
2020-10-20 08:00:58,1027605,962161,885389,...,9633
2020-10-20 08:30:58,1378375,1299526,1106099,...,13230
2020-10-20 09:00:59,1730790,1640496,1335244,...,16078
2020-10-20 09:30:58,1978380,1882941,1582188,...,18679
```

### gen_top3_border
The transition of the event points will be output to `. /output/{event_id}_top3_border.csv/`. The format is as follows.

```csv
datetime,{1st place username},{2nd place username},{3rd place username}
2021-07-20 15:01:58,,,
2021-07-20 15:30:58,439610.0,471100.0,333130.0
2021-07-20 16:00:58,1008850.0,1096375.0,885080.0
2021-07-20 16:30:58,1576830.0,1643180.0,1364685.0
2021-07-20 17:00:58,2148800.0,2264850.0,1917440.0
2021-07-20 17:30:58,2721995.0,2887990.0,2393510.0
2021-07-20 18:00:58,3293860.0,3510150.0,2942695.0
2021-07-20 18:30:58,3855540.0,4133815.0,3458770.0
2021-07-20 19:00:58,4452045.0,4720310.0,4012330.0
2021-07-20 19:30:58,5010960.0,5345865.0,4532360.0
```

### FAQ
There are no FAQ as of 2021-08-29.