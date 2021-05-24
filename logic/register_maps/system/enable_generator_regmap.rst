==============================
Enable generator register map
==============================

The shown register map is for the two output variant, for modules with more or less enable signals the corresponding treshold registers
should be used at proportionally increasing offsets 

+---------------+-----------------+-----------------+----------------+------------------------------------+
| Register Name | Register offset | Field name      | Field position | Description                        |
+===============+=================+=================+================+====================================+
| ENABLE        | 0x0             | enable          | 0              | Start the enable generator         |
+---------------+-----------------+-----------------+----------------+------------------------------------+
| PERIOD        | 0x4             | period_value    | 31:0           | Period of the output enable events |
+---------------+-----------------+-----------------+----------------+------------------------------------+
| THRESHOLD_1   | 0x8             | threshold_value | 31:0           | First enable event treshold        |
+---------------+-----------------+-----------------+----------------+------------------------------------+
| THRESHOLD_2   | 0xC             | threshold_value | 31:0           | Second enable event treshold       |
+---------------+-----------------+-----------------+----------------+------------------------------------+