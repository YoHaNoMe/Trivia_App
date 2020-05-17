import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/QuizView.css';

const questionsPerPlay = 10;

class QuizView extends Component {
  constructor(props){
    super();
    this.state = {
        quizCategory: null,
        previousQuestions: [],
        showAnswer: false,
        categories: [],
        numCorrect: 0,
        currentQuestion: {},
        guess: '',
        forceEnd: false
    }
  }

  componentDidMount(){
    $.ajax({
      url: `/api/categories`, //TODO: update request URL (Completed)
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }

  selectCategory = ({type, id=0}) => {
    this.setState({quizCategory: {type, id}}, this.getFirstQuestion)
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  getFirstQuestion = () => {
    $.ajax({
      url: '/api/quizzes?category=' + this.state.quizCategory.id,
      type: 'GET',
      success: (result) => {
        console.log(result)
        this.setState({
          showAnswer: false,
          currentQuestion: result.question,
          guess: '',
          forceEnd: !result.success
        })
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
        return;
      }
    })
  }

  getNextQuestion = () => {
    const previousQuestions = [...this.state.previousQuestions]
    if(this.state.currentQuestion.id) { previousQuestions.push(this.state.currentQuestion.id) }
    console.log(previousQuestions)
    console.log(this.state.quizCategory.id)
    var url = '/api/quizzes?category='+this.state.quizCategory.id
    for (var i = 0; i < previousQuestions.length; i++) {
      url+='&prev_question=' + previousQuestions[i]
    }
    console.log('Url: ' + url)
    $.ajax({
      url: url, //TODO: update request URL (Completed)
      type: "GET",
      success: (result) => {
        console.log(result)
        console.log('End: ' + !result.question)
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false: true
        })
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
        return;
      }
    })
  }

  submitGuess = (event) => {
    event.preventDefault();
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    let evaluate =  this.evaluateAnswer()
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true,
    })
  }

  restartGame = () => {
    this.setState({
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false
    })
  }

  renderPrePlay(){
      return (
          <div className="quiz-play-holder">
              <div className="choose-header">Choose Category</div>
              <div className="category-holder">
                  <div className="play-category" onClick={this.selectCategory}>ALL</div>
                  {
                  this.state.categories.map(category => {
                    // console.log(category)
                    return (
                      <div
                        key={category.id}
                        value={category.id}
                        className="play-category"
                        onClick={() => this.selectCategory({type:category.type, id:category.id})}
                        >
                        {category.type}
                      </div>
                    )}

                  // {Object.keys(this.state.categories).map(id => {
                  // return (
                  //   <div
                  //     key={id}
                  //     value={id}
                  //     className="play-category"
                  //     onClick={() => this.selectCategory({type:this.state.categories[id], id})}>
                  //     {this.state.categories[id]}
                  //   </div>
                  // )
                // }
              )}
              </div>
          </div>
      )
  }

  renderFinalScore(){
    return(
      <div className="quiz-play-holder">
        <div className="final-header"> Your Final Score is {this.state.numCorrect}</div>
        <div className="play-again button" onClick={this.restartGame}> Play Again? </div>
      </div>
    )
  }

  evaluateAnswer = () => {
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    const answerArray = this.state.currentQuestion.answer.toLowerCase().split(' ');
    return answerArray.includes(formatGuess)
  }

  renderCorrectAnswer(){
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    let evaluate =  this.evaluateAnswer()
    return(
      <div className="quiz-play-holder">
        <div className="quiz-question">{this.state.currentQuestion.question}</div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>{evaluate ? "You were correct!" : "You were incorrect"}</div>
        <div className="quiz-answer">{this.state.currentQuestion.answer}</div>
        <div className="next-question button" onClick={this.getNextQuestion}> Next Question </div>
      </div>
    )
  }

  renderPlay(){
    return this.state.previousQuestions.length === questionsPerPlay || this.state.forceEnd
      ? this.renderFinalScore()
      : this.state.showAnswer
        ? this.renderCorrectAnswer()
        : (
          <div className="quiz-play-holder">
            <div className="quiz-question">{this.state.currentQuestion.question}</div>
            <form onSubmit={this.submitGuess}>
              <input type="text" name="guess" onChange={this.handleChange}/>
              <input className="submit-guess button" type="submit" value="Submit Answer" />
            </form>
          </div>
        )
  }


  render() {
    return this.state.quizCategory
        ? this.renderPlay()
        : this.renderPrePlay()
  }
}

export default QuizView;
