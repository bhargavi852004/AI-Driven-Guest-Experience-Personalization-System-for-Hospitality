**Appendix: Milestone 3 - Hotel Review Analysis System**

## **Overview**
Milestone 3 involved integrating Together AI embeddings, Pinecone for vector storage, and Streamlit for building an interactive UI. The project focused on processing hotel customer reviews, generating embeddings, storing them in a Pinecone index, retrieving relevant reviews, analyzing sentiments, and providing a manager-friendly review analysis dashboard.

## **Customer Review Submission UI**
- **Features**:
  - Customers submit hotel reviews in real-time.
- **Sentiment Analysis**:
    - Used `TextBlob` to calculate sentiment score.
    - If a **negative** review is submitted and the customer is **currently staying**, an automated email with **room number, review, and sentiment score** is sent to the hotel manager.
## **Manager Review Analysis UI**
- **Built Using**: `Streamlit`
- **Key Functionalities**:
  - **Query Input**: Allows managers to ask review-related questions.
  - **Relevant Review Retrieval**: Uses Pinecone similarity search.
  - **Summarization**: Together AI generates a professional summary of customer sentiments.
  - **Word Cloud Generation**: Highlights frequently mentioned words based on the manager's query.
  - **Data Download**: Managers can download the sentiment analysis report as a `.txt` file.

## **Final Outcomes**
✅ Efficient storage and retrieval of customer reviews using Pinecone.
✅ AI-powered summarization for quick managerial insights.
✅ Real-time sentiment detection and manager notifications.
✅ User-friendly Streamlit dashboard for customer and manager interactions.
✅ Visualization enhancements using word clouds and sentiment scores.

## **UI Outcomes Images**
### **Customer Review Submission UI**
![sentiment](https://github.com/user-attachments/assets/41919237-b58a-48b2-a754-e6f430ad10c4)
![sentiment2](https://github.com/user-attachments/assets/d80d7bd6-045b-46df-acc4-79db97e8e9dc)
![sentiment3](https://github.com/user-attachments/assets/76fb0c4e-4e0f-45b5-850f-bbd32782f1a8)
![sentiment4](https://github.com/user-attachments/assets/00b16154-ea2a-4644-8662-2a0b7c47c3ea)
### **Manager Review Analysis UI**
![manager1](https://github.com/user-attachments/assets/d4494f3d-19ce-41fc-b7d6-49ad6a23d3bc)
![manager2](https://github.com/user-attachments/assets/31195bc8-0632-47b3-b394-6fdb4b861e3f)





