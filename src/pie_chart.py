import matplotlib.pyplot as plt
import mysql.connector

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": os.getenv("DB_PORT"),
}

def fetch_status_counts():
    query = """
    SELECT 
        status, COUNT(*) 
    FROM 
        domains 
    GROUP BY 
        status
    """
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data
  
def generate_chart(data):
    statuses = [row[0] for row in data]
    counts = [row[1] for row in data]
    total_domains = sum(counts)

    colors = {
        "unchecked": "#cccccc",
        "NOERROR": "#4caf50",
        "NXDOMAIN": "#f44336",
        "SERVFAIL": "#2196f3",
        "REFUSED": "#ff9800",
        "TIMEOUT": "#9c27b0",
        "OTHER": "#607d8b"
    }

    # Create pie chart
    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=statuses,
        autopct='%1.1f%%',
        colors=[colors.get(status, "#333333") for status in statuses],
        startangle=140
    )
  
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_fontsize(10)

    plt.title('Domain Status Distribution', fontsize=16)
    plt.figtext(0.5, 0.02, f'Total Domains: {total_domains}', ha='center', fontsize=12)

    output_path = "img/pie_chart.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_path}")

# Main execution
if __name__ == "__main__":
    data = fetch_status_counts()
    generate_chart(data)
