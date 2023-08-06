module BOLTX0004_B1024( bolt_length, head_diameter, head_height, head_shape )
{
    /*
        Description: This type or function is designated for simulating bolts when used in an assembly.
        Schema:
        Example:
    */

    if (head_shape == "HEX")
    {
        $fn=6;
        cylinder(h = head_height, r1 = head_diameter/2, r2 = head_diameter/2, center = true);
        
    }
    $fn = 50;
    translate([0,0,head_height/2+ bolt_length/2]){cylinder(h = bolt_length, r1 = 4.826/2, r2 = 4.826/2, center = true);}
}

module BOLTX0004_B832( bolt_length, head_diameter, head_height, head_shape )
{
    /*
        Description: This type or function is designated for simulating bolts when used in an assembly.
        Schema:
        Example:
    */

    if (head_shape == "HEX")
    {
        $fn=6;
        cylinder(h = head_height, r1 = head_diameter/2, r2 = head_diameter/2, center = true);
        
    }
    $fn = 50;
    translate([0,0,head_height/2+ bolt_length/2]){cylinder(h = bolt_length, r1 = 2.08, r2 = 2.08, center = true);}
}

module BOLTX0004_N1024( head_diameter, head_height, head_shape )
{
    /*
        Description:
        Schema:
        Example:
        Driver: boltx0004.py
    */

    if (head_shape == "TRI")
    {
        difference()
        {
            cylinder(h = head_height, r1 = head_diameter/2, r2 = head_diameter/2, center = true, $fn=3);
            translate([0,0,0]){ cylinder( h = head_height+0.01, r1 = 4.826/2, r2 = 4.826/2, center = true, $fn = 50); }
        }
        
    }
    if (head_shape == "HEX")
    {
        difference()
        {
            cylinder(h = head_height, r1 = head_diameter/2, r2 = head_diameter/2, center = true, $fn=6);
            translate([0,0,0]){ cylinder( h = head_height+0.01, r1 = 4.826/2, r2 = 4.826/2, center = true, $fn = 50); }
        }
            
    }

    if (head_shape == "TET")
    {
        difference()
        {
            cylinder(h = head_height, r1 = head_diameter/2, r2 = head_diameter/2, center = true, $fn=4);
            translate([0,0,0]){ cylinder( h = head_height+0.01, r1 = 4.826/2, r2 = 4.826/2, center = true, $fn = 50); }
        }
    }

    if (head_shape == "PEN")
    {
        difference()
        {
            cylinder(h = head_height, r1 = head_diameter/2, r2 = head_diameter/2, center = true, $fn=5);
            translate([0,0,0]){ cylinder( h = head_height+0.01, r1 = 4.826/2, r2 = 4.826/2, center = true, $fn = 50); }
        }
    }
}

module BOLTX0004_N832( head_diameter, head_height, head_shape )
{
    /*
        Description:
        Schema:
        Example:
        Driver: boltx0004.py
    */

    if (head_shape == "TRI")
    {
        difference()
        {
            cylinder(h = head_height, r1 = head_diameter/2, r2 = head_diameter/2, center = true, $fn=3);
            translate([0,0,0]){ cylinder( h = head_height+0.01, r1 = 2.08, r2 = 2.08, center = true, $fn = 50); }
        }
        
    }
    if (head_shape == "HEX")
    {
        difference()
        {
            cylinder(h = head_height, r1 = head_diameter/2, r2 = head_diameter/2, center = true, $fn=6);
            translate([0,0,0]){ cylinder( h = head_height+0.01, r1 = 2.08, r2 = 2.08, center = true, $fn = 50); }
        }
            
    }

    if (head_shape == "TET")
    {
        difference()
        {
            cylinder(h = head_height, r1 = head_diameter/2, r2 = head_diameter/2, center = true, $fn=4);
            translate([0,0,0]){ cylinder( h = head_height+0.01, r1 = 2.08, r2 = 2.08, center = true, $fn = 50); }
        }
    }

    if (head_shape == "PEN")
    {
        difference()
        {
            cylinder(h = head_height, r1 = head_diameter/2, r2 = head_diameter/2, center = true, $fn=5);
            translate([0,0,0]){ cylinder( h = head_height+0.01, r1 = 2.08, r2 = 2.08, center = true, $fn = 50); }
        }

            
    }
}

/* Tests */

// BOLTX0004_B1024( bolt_length = 50.8, head_diameter = 9, head_height = 3, head_shape = "HEX" ); // BOLTX0004-S1024-HEX-L50P8D9H3
// BOLTX0004_B832( bolt_length = 50.8, head_diameter = 9, head_height = 3, head_shape = "HEX" ); // BOLTX0004-S1024-HEX-L50P8D9H3
// BOLTX0004_N1024( head_diameter = 13, head_height = 3, head_shape = "TRI" );
// BOLTX0004_N832( head_diameter = 13, head_height = 3, head_shape = "HEX" );