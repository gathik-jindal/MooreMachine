import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import javax.swing.JTextArea;

import java.io.File;

public class GenerateFile 
{
    private PrintWriter pw;

    public GenerateFile(ArrayList<Block> block, ArrayList<Block> wires, JTextArea area, int generateCSV, int time)
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

        if(generateCSV == 0)
            pw.println("pysim.generateCSV()");
        pw.println("pysim.run(until = " + time + ")");

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

                String outputMSB = wire.getOutputMSB(), outputLSB = wire.getOutputLSB();
                
                String outputString = ".output";
                String inputString = ".input";
                
                if(startBlock instanceof Clock && endBlock instanceof Moore && wire.isClocked())
                    inputString = ".clock";

                if(outputMSB == null || outputLSB == null)
                    pw.print(startBlock.getObjectName() + outputString + "() > ");
                else
                    pw.print(startBlock.getObjectName() + outputString + "(" + outputLSB + ", " + outputMSB + ") > ");
                
                pw.println(endBlock.getObjectName() + inputString + "()");
            }
        }
    }
}
