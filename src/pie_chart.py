import os
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

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, _ = ax.pie(
        counts,
        colors=[colors.get(status, "#333333") for status in statuses],
        startangle=140
    )

    ax.set_title('Domain Status Distribution', fontsize=16)

    legend_labels = [
        f"{status}: {count} ({count / total_domains:.1%})"
        for status, count in zip(statuses, counts)
    ]
    ax.legend(
        wedges,
        legend_labels,
        title="Statuses",
        loc="center left",
        bbox_to_anchor=(0.9, 0.5),
        fontsize=10
    )

    output_dir = "img"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "pie_chart.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    data = fetch_status_counts()
    generate_chart(data)
