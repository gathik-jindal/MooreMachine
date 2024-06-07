import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Point;
import java.awt.Rectangle;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.SwingUtilities;

public class DrawingApp extends JFrame 
{
    private Manager manage;

    public DrawingApp() 
    {
        super("Moore Machine Simulator");
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(1500, 800);
        this.setResizable(false);
        manage = new Manager();

        this.add(manage);

        this.setVisible(true);
        this.requestFocusInWindow();
    }

    public static void main(String[] args) 
    {
        new DrawingApp();
    }
}

class MenuBar extends JMenuBar 
{
    private JMenu drawMenu;
    private Item input, clock, moore, comb, output, wire;
    
    public MenuBar(Manager manage) 
    {
        drawMenu = new JMenu("Select Type");
        input = new Item(Manager.Blocks.INPUT, DrawingPanel.Mode.BOX, Color.ORANGE, manage);
        clock = new Item(Manager.Blocks.CLOCK, DrawingPanel.Mode.BOX, Color.BLUE, manage);
        moore = new Item(Manager.Blocks.MOORE, DrawingPanel.Mode.BOX, Color.GREEN, manage);
        comb = new Item(Manager.Blocks.COMB, DrawingPanel.Mode.BOX, Color.RED, manage);
        output = new Item(Manager.Blocks.OUTPUT, DrawingPanel.Mode.BOX, Color.PINK, manage);
        wire = new Item(Manager.Blocks.WIRE, DrawingPanel.Mode.LINE, Color.BLACK, manage);

        drawMenu.add(input);
        drawMenu.add(clock);
        drawMenu.add(moore);
        drawMenu.add(comb);
        drawMenu.add(output);
        drawMenu.add(wire);
        
        this.add(drawMenu);
    }
}

class Item extends JMenuItem 
{
    public Item(Manager.Blocks title, DrawingPanel.Mode mode, Color color, Manager manage) 
    {
        super(title.getName());

        this.addActionListener(e -> 
        {
            manage.getDrawingPanel().setDrawingMode(mode, color, title);
            manage.getDrawingPanel().setCursor(Cursor.getPredefinedCursor(Cursor.CROSSHAIR_CURSOR));
        });
    }
}

class Manager extends JPanel 
{
    private MenuBar bar;
    private DrawingPanel drawingPanel;
    private InfoPanel infoPanel;
    
    public enum Blocks
    {
        INPUT("Input Block"), MOORE("Moore Machine"), COMB("Combinational Block"), 
        OUTPUT("Output Block"), CLOCK("Clock"), WIRE("Wire");

        private String name;

        private Blocks(String name)
        {
            this.name = name;
        }

        public String getName()
        {
            return name;
        }
    }

    public Manager() 
    {
        super(new BorderLayout());
        
        bar = new MenuBar(this);
        this.add(bar, BorderLayout.NORTH);

        drawingPanel = new DrawingPanel(this);
        this.add(drawingPanel, BorderLayout.CENTER);

        infoPanel = new InfoPanel(this);
        this.add(infoPanel, BorderLayout.WEST);
    }

    public DrawingPanel getDrawingPanel() 
    {
        return drawingPanel;
    }

    public InfoPanel getInfoPanel() 
    {
        return infoPanel;
    }

    public Block createBlock(Blocks block, Rectangle rect, Color color)
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
                return new Wire(block.getName(), rect, color, drawingPanel);
            default:
                return null;
        }
    }
}

class InfoPanel extends JPanel 
{
    private Map<String, Component> infoMap;
    private JPanel infoPanel;
    private JTextArea textArea;

    public InfoPanel(Manager manage) 
    {
        this.setLayout(new BorderLayout());
        this.setPreferredSize(new Dimension(350, 0));

        JLabel headerLabel = new JLabel("Right click on block to get information about it");
        headerLabel.setFont(new Font("Arial", Font.BOLD, 13));
        headerLabel.setForeground(Color.BLUE);
        headerLabel.setHorizontalAlignment(JLabel.CENTER);
        headerLabel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        this.add(headerLabel, BorderLayout.NORTH);

        infoPanel = new JPanel();
        infoPanel.setLayout(new GridBagLayout());
        infoPanel.setBackground(Color.YELLOW);
        infoPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        this.add(infoPanel, BorderLayout.CENTER);

        JPanel southPanel = new JPanel(new BorderLayout());

        JButton generateFile = new JButton("Generate Code");
        generateFile.setFont(new Font("Arial", Font.BOLD, 13));
        generateFile.setBackground(new Color(173, 216, 230));
        generateFile.setHorizontalAlignment(JButton.CENTER);
        generateFile.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        generateFile.addMouseListener(new MouseAdapter() 
        {
            @Override
            public void mouseEntered(MouseEvent evt) 
            {
                generateFile.setBackground(Color.CYAN);
            }

            @Override
            public void mouseExited(MouseEvent evt) 
            {
                generateFile.setBackground(new Color(173, 216, 230));
            }
        });

        generateFile.addActionListener(new ActionListener() 
        {

            @Override
            public void actionPerformed(ActionEvent e) 
            {
                new GenerateFile(manage.getDrawingPanel().getRectangles(), getTextArea());
            } 
        });

        southPanel.add(generateFile, BorderLayout.SOUTH);

        JPanel centerPanel = new JPanel(new BorderLayout());

        JLabel functions = new JLabel("Add Functions Here:");
        functions.setFont(new Font("Arial", Font.BOLD, 13));
        functions.setForeground(Color.BLUE);
        functions.setHorizontalAlignment(JLabel.CENTER);
        functions.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        textArea = new JTextArea("");
        textArea.setLineWrap(true);
        textArea.setWrapStyleWord(true);
        textArea.setTabSize(4);

        JScrollPane scrollPane = new JScrollPane(textArea);
        scrollPane.setPreferredSize(new Dimension(200, 200));

        centerPanel.add(functions, BorderLayout.NORTH);
        centerPanel.add(scrollPane, BorderLayout.CENTER);

        southPanel.add(centerPanel, BorderLayout.CENTER);

        this.add(southPanel, BorderLayout.SOUTH);

        infoMap = new LinkedHashMap<>();
    }

    public void updateInfo(Map<String, Component> info) 
    {
        infoPanel.removeAll();

        for (String label : info.keySet()) 
        {
            JLabel jLabel = new JLabel(label);
            jLabel.setFont(new Font("Arial", Font.BOLD, 12));
            jLabel.setForeground(Color.DARK_GRAY);
            jLabel.setHorizontalAlignment(JLabel.CENTER);

            GridBagConstraints gbc = new GridBagConstraints();
            gbc.fill = GridBagConstraints.HORIZONTAL;
            gbc.weightx = 1.0;
            gbc.gridx = 0;
            gbc.gridy = GridBagConstraints.RELATIVE;
            gbc.anchor = GridBagConstraints.CENTER;

            Component comp = info.get(label);
            infoMap.put(label, comp);

            infoPanel.add(jLabel, gbc);

            gbc.gridy = GridBagConstraints.RELATIVE;
            infoPanel.add(javax.swing.Box.createVerticalStrut(5), gbc);

            gbc.gridy = GridBagConstraints.RELATIVE;
            infoPanel.add(comp, gbc);

            gbc.gridy = GridBagConstraints.RELATIVE;
            infoPanel.add(javax.swing.Box.createVerticalStrut(10), gbc);
        }

        this.revalidate();
        this.repaint();
    }

    public JTextArea getTextArea()
    {
        return this.textArea;
    }
}

class DrawingPanel extends JPanel 
{
    public enum Mode { NONE, BOX, LINE }
    private Mode drawingMode = Mode.NONE;
    private Point startPoint;
    private ArrayList<Block> rectangles;
    private Rectangle currentRect;
    private Color currentColor;
    private Manager.Blocks currentName;
    private Manager manager;
    private boolean isDragging;

    public DrawingPanel(Manager manager) 
    {
        this.manager = manager;
        setBackground(Color.WHITE);

        rectangles = new ArrayList<>();
        isDragging = false;
        
        MouseAdapter mouseAdapter = new MouseAdapter() 
        {
            @Override
            public void mousePressed(MouseEvent e) 
            {
                if (SwingUtilities.isRightMouseButton(e)) 
                {
                    handleRightClick(e.getPoint());
                } 
                else if (drawingMode == Mode.BOX) 
                {
                    startPoint = e.getPoint();
                    currentRect = new Rectangle(startPoint);
                    repaint();
                }
            }

            @Override
            public void mouseDragged(MouseEvent e) 
            {
                if (drawingMode == Mode.BOX && startPoint != null) 
                {
                    isDragging = true;
                    updateRectangle(e.getPoint());
                    repaint();
                }
            }

            @Override
            public void mouseReleased(MouseEvent e) 
            {
                if (drawingMode == Mode.BOX && startPoint != null) 
                {
                    if(isDragging)
                    {
                        updateRectangle(e.getPoint());
                        isDragging = false;

                        if(!isIntersecting(currentRect))    
                        {
                            rectangles.add(manager.createBlock(currentName, currentRect, currentColor));
                            handleRightClick(new Point(currentRect.x + currentRect.width/2, currentRect.y + currentRect.height/2));
                        }
                    }

                    repaint();
                    startPoint = null;
                    currentRect = null;            
                }
            }
        };

        addMouseListener(mouseAdapter);
        addMouseMotionListener(mouseAdapter);
    }

    private void handleRightClick(Point point) 
    {
        for (Block block : rectangles) 
        {
            if (block.getRect().contains(point)) 
            {
                manager.getInfoPanel().updateInfo(block.getMap());
                return;
            }
        }
    }

    public void setDrawingMode(Mode mode, Color color, Manager.Blocks name) 
    {
        this.drawingMode = mode;
        this.currentColor = color;
        this.currentName = name;
    }

    private void updateRectangle(Point endPoint) 
    {
        int x = Math.min(startPoint.x, endPoint.x);
        int y = Math.min(startPoint.y, endPoint.y);
        int width = Math.abs(startPoint.x - endPoint.x);
        int height = Math.abs(startPoint.y - endPoint.y);
        currentRect.setBounds(x, y, width, height);
    }

    @Override
    protected void paintComponent(Graphics g) 
    {
        super.paintComponent(g);
        if (currentRect != null) 
        {
            g.setColor(currentColor);
            g.fillRect(currentRect.x, currentRect.y, currentRect.width, currentRect.height);
            g.setColor(Color.black);
            Graphics2D g2 = (Graphics2D) g;
            g2.setStroke(new BasicStroke(3));
            g2.drawRect(currentRect.x, currentRect.y, currentRect.width, currentRect.height);
        }

        for (Block block : rectangles) 
        {
            Rectangle rect = block.getRect();
            g.setColor(block.getColor());
            g.fillRect(rect.x, rect.y, rect.width, rect.height);
            g.setColor(Color.black);
            Graphics2D g2 = (Graphics2D) g;
            g2.setStroke(new BasicStroke(2));
            g2.drawRect(rect.x, rect.y, rect.width, rect.height);
            g.setFont(new Font("Arial", Font.BOLD, 15));
            FontMetrics metrics = g.getFontMetrics();
            int textWidth = metrics.stringWidth(block.getName());
            int textHeight = metrics.getHeight();
            int textX = rect.x + (rect.width - textWidth) / 2;
            int textY = rect.y + (rect.height - textHeight) / 2 + metrics.getAscent();
            g.drawString(block.getName(), textX, textY);
        }
    }

    public boolean isIntersecting(Rectangle r1) 
    {
        for(Block block:rectangles)
        {
            if(block.getRect().intersects(r1))
                return true;
        }

        return false;
    }

    public ArrayList<Block> getRectangles()
    {
        return rectangles;
    }
}