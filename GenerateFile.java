/**
 * This is the GenerateFile class that generates the python file "simulation.py". 
 * 
 * @author Aryan, Abhirath, Gathik
 * @version 1.0
 * @since 06/08/2024
 */

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import javax.swing.JTextArea;

import java.io.File;

public class GenerateFile 
{
    private PrintWriter pw; //PrintWrite object to write in the path specified by the user

    /**
     * Creates a GenerateFile object.
     * @param block : an ArrayList object that contains all rectangular blocks
     * @param wires : an ArrayList object that contains all wires
     * @param area : the JTextArea object with funtions
     * @param generateCSV : 0 to generate csv; otherwise, csv would not be generated
     * @param time : the time duration to run the simulation for
     * @throws IOException : if File IO resulted in an error
     */
    public GenerateFile(String path, ArrayList<Block> block, ArrayList<Block> wires, JTextArea area, int generateCSV, int time) throws IOException
    {
        pw = new PrintWriter(new FileWriter(new File(path)));
        
        writeImport();
        writeFunctions(area);
        writeBlock(block);
        writeWire(wires);

        if(generateCSV == 0)
            pw.println("pysim.generateCSV()");
        pw.println("pysim.run(until = " + time + ")");

        pw.close();

    }    

    /**
     * Write the import statements in the file.
     */
    private void writeImport()
    {
        pw.println("import pydig\n");
        pw.println("pysim = pydig.pydig(name = \"Pydig\")\n");
    }

    /**
     * Write the different functions
     * @param area : the JTextArea containing the functions.
     */
    private void writeFunctions(JTextArea area)
    {
        pw.println(area.getText() + "\n");
    }

    /**
     * Writes the information present in the rectangular blocks
     * @param block : ArrayList object holding all the rectangular blocks
     */
    private void writeBlock(ArrayList<Block> block)
    {
        for(Block b : block)
            pw.println(b);
    }

    /**
     * Writes the information present in the wires
     * @param wires : ArrayList object holding all the wires
     */
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
