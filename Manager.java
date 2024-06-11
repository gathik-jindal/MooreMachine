/**
 * This is the manager class that holds all the JPanels. 
 * 
 * @author Aryan, Abhirath, Gathik
 * @version 1.0
 * @since 06/08/2024
 */

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.event.WindowEvent;
import java.awt.geom.Line2D;

import java.awt.image.BufferedImage;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;

import javax.imageio.ImageIO;

import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSlider;
import javax.swing.JTextArea;
import javax.swing.filechooser.FileNameExtensionFilter;

public abstract class Manager extends JPanel 
{
    private MenuBar bar;                //The MenuBar that goes at the top of the Panel
    private JSlider zoomSlider;         //Controls the level of zooming in and out
    private DrawCircuit drawingPanel;  //The drawing panel that goes in the center of the Panel
    private InfoPanel infoPanel;        //The information panel that allows the user to look at information regarding the blocks 
    private DrawingApp frame;               //The frame object.

    /**
     * The blocks enum which stores the name of the blocks.
     */
    public enum Blocks
    {
        INPUT("Input Block"), MOORE("Moore Machine"), COMB("Combinational Block"), 
        OUTPUT("Output Block"), CLOCK("Clock"), WIRE("Wire");

        private String name;            //The name of the block

        /**
         * Sets the name of the block
         * @param name : the name of the block
         */
        private Blocks(String name)
        {
            this.name = name;
        }

        /**
         * @return the name of the block
         */
        public String getName()
        {
            return name;
        }
    }

    /**
     * Creates a manager object.
     * @param frame : the frame in which this panel would be placed in
     */
    public Manager(DrawingApp frame) 
    {
        super(new BorderLayout());
        
        bar = new MenuBar(this);

        this.add(bar, BorderLayout.NORTH);

        drawingPanel = new DrawCircuit(this);
        JScrollPane scrollPane = new JScrollPane(drawingPanel);
        this.add(scrollPane, BorderLayout.CENTER);

        zoomSlider = new JSlider(50, 200, 100);
        
        zoomSlider.setMajorTickSpacing(25);
        zoomSlider.setMinorTickSpacing(5);
        zoomSlider.setPaintTicks(true);
        zoomSlider.setPaintLabels(true);

        Hashtable<Integer, JLabel> labelTable = new Hashtable<>();
        for(int i = 50; i <= 200; i += 25)
            labelTable.put(i, new JLabel(i+"%"));
        zoomSlider.setLabelTable(labelTable);

        zoomSlider.addChangeListener(e -> 
        {
            drawingPanel.setZoom(zoomSlider.getValue() / 100.0);
        });
        
        this.add(zoomSlider, BorderLayout.SOUTH);

        infoPanel = new InfoPanel(this);
        this.add(infoPanel, BorderLayout.WEST);

        this.frame = frame;

        Item [] items = getItems();
        for(Item item : items)
            bar.addMenuItem(item);
    }

    /**
     * @return the drawing panel object
     */
    public DrawCircuit getDrawCircuit() 
    {
        return drawingPanel;
    }

    /**
     * @return the info panel object
     */
    public InfoPanel getInfoPanel() 
    {
        return infoPanel;
    }

    public int getZoomValue()
    {
        return zoomSlider.getValue();
    }

    public void setZoomValue(int val)
    {
        if(zoomSlider.getValue() + val <= zoomSlider.getMaximum() && zoomSlider.getValue() + val >= zoomSlider.getMinimum())
        {
            zoomSlider.setValue(zoomSlider.getValue() + val);
        }
    }

    /**
     * Creates a new block from the inputs specified.
     * If the block is a Wire, then a line is added. Otherwise, a rectangle is added.
     * @param block : The type of block you want
     * @param line : a line object to represent a wire
     * @param rect : a rectangle object to represent all other blocks
     * @param color : the color of this block
     * @return a new Block object
     */
    public Block createBlock(Blocks block, Line2D.Double line, Rectangle rect, Color color)
    {
        switch(block)
        {
            case INPUT:
                return new Input(block.getName(), rect, color, drawingPanel);
            case OUTPUT:
                return new Output(block.getName(), rect, color, drawingPanel);
            case MOORE:
                return new Moore(block.getName(), rect, color, drawingPanel);
            case CLOCK:
                return new Clock(block.getName(), rect, color, drawingPanel);
            case COMB:
                return new Combinational(block.getName(), rect, color, drawingPanel);
            case WIRE:
                return new Wire(block.getName(), line, color, drawingPanel);
            default:
                return null;
        }
    }

    /**
     * This method sets the closest block for all the wires, i.e., the starting and the ending blocks that the wire connects.
     * @param showMessageDialog : whether or not to show any error messages
     * @return true if all wires have been connected properly; false otherwise
     */
    public boolean setClosestBlock(boolean showMessageDialog) 
    {
        ArrayList<Block> wires = drawingPanel.getWires();
        ArrayList<Block> rectangles = drawingPanel.getRectangles();
    
        double thresholdDistance = 400.0;
    
        for (Block wire : wires) 
        {
            Point [] endPoints;
            Point arrowTip = new Point(((Wire)(wire)).getArrowHead().xpoints[0], ((Wire)(wire)).getArrowHead().ypoints[0]);

            endPoints = new Point []
            {
                new Point((int)(wire.getLine().x1), (int)(wire.getLine().y1)),
                arrowTip
            };

            for (int i = 0; i < endPoints.length; i++) 
            {
                Point endPoint = endPoints[i];
                boolean isStartPoint = (i == 0);
                double closestDistance = Double.MAX_VALUE;
                Block closestBlock = null;
                
                //Loop through all the rectangles and see which rectangle is closest
                for (Block rectangle : rectangles) 
                {
                    Rectangle rect = rectangle.getRect();
                    Point[] rectPoints = 
                    {
                        new Point(rect.x, rect.y),
                        new Point(rect.x + rect.width, rect.y),
                        new Point(rect.x, rect.y + rect.height),
                        new Point(rect.x + rect.width, rect.y + rect.height)
                    };
    
                    for (Point rectPoint : rectPoints) 
                    {
                        double distance = endPoint.distance(rectPoint);
                        if (distance < closestDistance) 
                        {
                            closestDistance = distance;
                            closestBlock = rectangle;
                        }
                    }
                }
                
                //Loops through all the wires and sees which wire is the closest
                for (Block otherWire : wires) 
                {
                    if (otherWire == wire) continue;
    
                    Point[] wirePoints = 
                    {
                        new Point((int)(otherWire.getLine().x1), (int)(otherWire.getLine().y1)),
                        new Point((int)(otherWire.getLine().x2), (int)(otherWire.getLine().y2))
                    };
    
                    for (int j = 0; j < wirePoints.length; j++) 
                    {
                        Point wirePoint = wirePoints[j];
                        boolean isOtherStartPoint = (j == 0);
                        
                        //only allow those wires to be "close" to each other who have their opposite ends close together
                        if ((isStartPoint && !isOtherStartPoint) || (!isStartPoint && isOtherStartPoint)) 
                        {
                            double distance = endPoint.distance(wirePoint);
                            if (distance < closestDistance) 
                            {
                                closestDistance = distance;
                                closestBlock = otherWire;
                            }
                        }
                    }
                }
                
                //if the closest distance to any block is greater than the threshold, the connections have not been done properly.
                //In this case we return false.
                if (closestDistance > thresholdDistance) 
                {
                    if(showMessageDialog)
                        JOptionPane.showMessageDialog(null, "Invalid Connections. Check wire connections.", "Error", JOptionPane.ERROR_MESSAGE);
                    return false;
                }
                
                ((Wire)(wire)).setBlock(closestBlock);
            }
        }
        
        //Find the closest rectangular block
        for (Block wire : wires) 
        {
            Block currentBlock = ((Wire)(wire)).getStartBlock();
            Wire currentWire = (Wire)(wire);
            boolean foundRectangle = !(currentBlock instanceof Wire);
            
            //Loop through the wire connections until you get to one wire which has starting connection to a rectangle.
            while (currentBlock instanceof Wire) 
            {
                Wire connection = (Wire) currentBlock;
                Block endBlock = connection.getStartBlock();
                currentWire = connection;
                if (endBlock instanceof RectangleBlock) 
                {
                    foundRectangle = true;
                    currentBlock = endBlock;
                    break;
                }
                else if(currentBlock == endBlock)
                {
                    if(showMessageDialog)
                        JOptionPane.showMessageDialog(null, "Invalid Connections. Check wire connections.", "Error", JOptionPane.ERROR_MESSAGE);
                    return false;
                } 
                else 
                {
                    currentBlock = endBlock;
                }
            }
    
            if (foundRectangle) 
            {
                Wire connection = (Wire) wire;
                connection.setStartBlock(currentBlock, currentWire);
            } 
            else 
            {
                if(showMessageDialog)
                    JOptionPane.showMessageDialog(null, "Invalid Connections. Check wire connections.", "Error", JOptionPane.ERROR_MESSAGE);
                return false;
            }
        }
    
        return true;
    }
    
    /**
     * Checks if all the wires are connected to valid rectangles.
     * It is advised to first check if all the wires are actually connected or not via the above method.
     * @param wires : An ArrayList of Block that contains all wires
     * @return true if all connections are valid; false otherwise
     * @see setClosestBlock
     */
    public boolean isValidConnections(ArrayList<Block> wires)
    {
        for(Block w : wires)
        {
            Wire wire = (Wire)(w);
            if(wire.getStartBlock() instanceof RectangleBlock && wire.getEndBlock() instanceof RectangleBlock)
            {
                RectangleBlock startBlock = (RectangleBlock)(wire.getStartBlock());
                RectangleBlock endBlock = (RectangleBlock)(wire.getEndBlock());
                
                //startBlock needs to have output connections and endBlock needs to have input connections
                if(startBlock.hasOutput() && endBlock.hasInput()) continue;
                else if(startBlock.hasOutput())
                {
                    wires.remove(w);
                    drawingPanel.repaint();
                    JOptionPane.showMessageDialog(null, "Invalid wire detected and deleted. " + 
                        "Note: " + endBlock.getType() + " has no input connections.", "Error.", JOptionPane.ERROR_MESSAGE);
                    return false;
                }
                else
                {
                    wires.remove(w);
                    drawingPanel.repaint();
                    JOptionPane.showMessageDialog(null, "Invalid wire detected and deleted. " + 
                        "Note: " + startBlock.getType() + " has no output connections.", "Error.", JOptionPane.ERROR_MESSAGE);
                    return false;
                }
            }
        }

        return true;
    }

    /**
     * Allows the user to save the image.
     */
    public void saveImage() 
    {
        JFileChooser fileChooser = new JFileChooser();
        FileNameExtensionFilter filter = new FileNameExtensionFilter("PNG Images", "png");
        fileChooser.setFileFilter(filter);
        int returnValue = fileChooser.showSaveDialog(this);

        if (returnValue == JFileChooser.APPROVE_OPTION) 
        {
            File file = fileChooser.getSelectedFile();
            if (!file.getName().toLowerCase().endsWith(".png")) 
            {
                file = new File(file.getAbsolutePath() + ".png");
            }
            try 
            {
                BufferedImage image = new BufferedImage(drawingPanel.getWidth(), drawingPanel.getHeight(), BufferedImage.TYPE_INT_RGB);
                Graphics2D g2d = image.createGraphics();
                drawingPanel.paint(g2d);
                g2d.dispose();
                ImageIO.write(image, "png", file);
                JOptionPane.showMessageDialog(null, "Image saved successfully!", "Success", JOptionPane.INFORMATION_MESSAGE);
            } 
            catch (Exception ex) 
            {
                JOptionPane.showMessageDialog(null, "Failed to save image: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
        else
        {
            JOptionPane.showMessageDialog(null, "Failed to save image.", "Error", JOptionPane.ERROR_MESSAGE);
        }   
    }

    protected int getIntegerInput(String message)
    {
        boolean validInput = false;
        int number = 0;
        while (!validInput) 
        {
            String input = JOptionPane.showInputDialog(null, message);
            
            try 
            {
                number = Integer.parseInt(input);
                            validInput = true;
            } 
            catch (NumberFormatException exception) 
            {
                JOptionPane.showMessageDialog(null, "Invalid input. Please enter a valid integer.", "Error", JOptionPane.ERROR_MESSAGE);
            }
        }

        return number;
    }

    protected String getStringInput(String message, String title)
    {
        String ans = JOptionPane.showInputDialog(null, message, title, JOptionPane.QUESTION_MESSAGE);
        while(ans == null)
        {
            JOptionPane.showMessageDialog(null, "Invalid input. Please enter a valid String.", "Error", JOptionPane.ERROR_MESSAGE);
            ans = JOptionPane.showInputDialog(null, message, title, JOptionPane.QUESTION_MESSAGE);
        }

        return ans;
    }
    
    /**
     * @return the frame object that this class is part of
     */
    public JFrame getFrame()
    {
        return this.frame;
    }

    public void goHome()
    {
        int option = JOptionPane.showInternalConfirmDialog(null, "Do you want to go back to home page?", "Go home", JOptionPane.YES_NO_OPTION, JOptionPane.INFORMATION_MESSAGE);

        if(option == 0)
        {
            drawingPanel.clear();
            frame.change(DrawingApp.HOME);
        }
    }

    protected abstract Item [] getItems();
    protected abstract void generateFile(JTextArea area);
    protected abstract String getFunctionLabel();
}

class ManageMainCircuit extends Manager
{
    public ManageMainCircuit(DrawingApp frame)
    {
        super(frame);
    }

    protected Item [] getItems()
    {
        Item [] items = 
        {
            new Item(Manager.Blocks.INPUT, DrawCircuit.Mode.BOX, Color.ORANGE, this),
            new Item(Manager.Blocks.CLOCK, DrawCircuit.Mode.BOX, Color.BLUE, this),
            new Item(Manager.Blocks.MOORE, DrawCircuit.Mode.BOX, Color.GREEN, this),
            new Item(Manager.Blocks.COMB, DrawCircuit.Mode.BOX, Color.RED, this),
            new Item(Manager.Blocks.OUTPUT, DrawCircuit.Mode.BOX, Color.PINK, this),
            new Item(Manager.Blocks.WIRE, DrawCircuit.Mode.LINE, Color.BLACK, this),
        };

        return items;
    }

    protected void generateFile(JTextArea area)
    {
        int option = JOptionPane.showInternalConfirmDialog(null, "Do you want to generate a CSV file?", 
                            "Generate CSV File", JOptionPane.YES_NO_OPTION, JOptionPane.INFORMATION_MESSAGE);
                        
        int number = getIntegerInput("Please enter how much time you want to run for:");

        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Choose/Create a Python File");

        FileNameExtensionFilter filter = new FileNameExtensionFilter("Python Files", "py");
        fileChooser.setFileFilter(filter);

        int returnValue = fileChooser.showOpenDialog(null);

        try
        {
            if(returnValue != JFileChooser.APPROVE_OPTION)
                throw new IOException("Could not generate the code");
                File selectedFile = fileChooser.getSelectedFile();
                FileIO.generateCircuitFile(selectedFile.getAbsolutePath(), getDrawCircuit().getRectangles(), getDrawCircuit().getWires(), area, option, number);
                getFrame().dispatchEvent(new WindowEvent(getFrame(), WindowEvent.WINDOW_CLOSING));
        }
        catch(IOException exp)
        {
            JOptionPane.showMessageDialog(null, "Could not generate the code.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    protected String getFunctionLabel()
    {
        return "Add Functions Here:";
    }
}

/**
 * This class handles the menu bar that appears at the top of the page.
 */
class MenuBar extends JMenuBar 
{
    private JMenu drawMenu, fileMenu;                       //the draw menu allows the user to draw on the pannel, and the file menu allows the user to save the project
    private JMenuItem saveImage, home;                      //this item allows the user to save the image

    /**
     * Creates a Menubar and add the different items.
     * @param manage : The Manager JPanel object in which the bar would be placed
     */
    public MenuBar(Manager manage) 
    {
        fileMenu = new JMenu("File");
        saveImage = new JMenuItem("Save Image");
        home = new JMenuItem("Go to Home Page");

        saveImage.addActionListener(e -> manage.saveImage());
        fileMenu.add(saveImage);
        
        home.addActionListener(e -> manage.goHome());
        fileMenu.add(home);

        this.add(fileMenu);

        drawMenu = new JMenu("Add Component");

        this.add(drawMenu);
    }

    public void addMenuItem(JMenuItem item)
    {
        drawMenu.add(item);
    }
}

/**
 * This class handles each JMenuItem that appears in the JMenu.
 */
class Item extends JMenuItem 
{
    /**
     * Creates a JMenuItem.
     * @param title : the type of block this Item is
     * @param mode : the drawing mode that is initiated when this item is clicked
     * @param color : the color of the object which would be drawn
     * @param manage : the Manager class which has the JPanels
     */
    public Item(Manager.Blocks title, DrawCircuit.Mode mode, Color color, Manager manage) 
    {
        super(title.getName());

        this.addActionListener(e -> 
        {
            manage.getDrawCircuit().setDrawingMode(mode, color, title);
            manage.getDrawCircuit().setCursor(Cursor.getPredefinedCursor(Cursor.CROSSHAIR_CURSOR));
        });
    }
}