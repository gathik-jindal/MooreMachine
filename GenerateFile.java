import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import javax.swing.JTextArea;

import java.io.File;

public class GenerateFile 
{
    private PrintWriter pw;

    public GenerateFile(ArrayList<Block> block, ArrayList<Block> wires, JTextArea area)
    {
        try
        {
            pw = new PrintWriter(new FileWriter(new File("simulation.py")));
        }
        catch(IOException e)
        {
            System.err.println("Cannot edit simulation.py");
        }

        writeImport();
        writeFunctions(area);
        writeBlock(block);
        writeWire(wires);

        pw.close();
    }    

    private void writeImport()
    {
        pw.println("import pydig\n");
        pw.println("pysim = pydig.pydig(name = \"Pydig\")\n");
    }

    private void writeFunctions(JTextArea area)
    {
        pw.println(area.getText() + "\n");
    }

    private void writeBlock(ArrayList<Block> block)
    {
        for(Block b : block)
            pw.println(b);
    }

    private void writeWire(ArrayList<Block> wires)
    {
        for(Block w : wires)
        {
            Wire wire = (Wire)(w);
            if(wire.getStartBlock() instanceof RectangleBlock && wire.getEndBlock() instanceof RectangleBlock)
            {
                RectangleBlock startBlock = (RectangleBlock)(wire.getStartBlock());
                RectangleBlock endBlock = (RectangleBlock)(wire.getEndBlock());

                pw.println(startBlock.getObjectName() + ".output() > " + endBlock.getObjectName() + ".input()");
            }
        }
    }
}
